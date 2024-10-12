import pytest
from unittest.mock import patch, MagicMock
from twilio.rest import Client as TwilioRestClient

from strideutils.twilio_connector import TwilioClient

@pytest.fixture
def mock_twilio_client():
    with patch('strideutils.twilio_connector.Client') as mock_client:
        yield mock_client.return_value

@pytest.fixture
def twilio_client(mock_twilio_client):
    with patch('strideutils.twilio_connector.get_env_or_raise') as mock_get_env:
        mock_get_env.side_effect = ['fake_account_id', 'fake_api_token', 'fake_alert_numbers']
        client = TwilioClient()
        client.client = mock_twilio_client  # Replaced the real Twilio client with a mock, to not send to the real.
        yield client

def test_twilio_client_singleton():
    with patch('strideutils.twilio_connector.Client'):
        with patch('strideutils.twilio_connector.get_env_or_raise'):
            client1 = TwilioClient()
            client2 = TwilioClient()
            assert client1 is client2

def test_call_single_recipient(twilio_client, mock_twilio_client):
    with patch('strideutils.twilio_connector.config') as mock_config:
        mock_config.PHONE_NUMBERS = {'recipient': '+12223334444'}
        mock_config.TWILIO_ALERTS_NUMBER = '+15556667777'

        twilio_client.call("Test message", "recipient")

        expected_twiml = "<Response><Say>Test message</Say></Response>"
        mock_twilio_client.calls.create.assert_called_once_with(
            to='+12223334444',
            from_='+15556667777',
            twiml=expected_twiml
        )

def test_call_multiple_recipients(twilio_client, mock_twilio_client):
    with patch('strideutils.twilio_connector.config') as mock_config:
        mock_config.PHONE_NUMBERS = {
            'recipient1': '+12223334444',
            'recipient2': '+13334445555'
        }
        mock_config.TWILIO_ALERTS_NUMBER = '+15556667777'

        twilio_client.call("Test message", ["recipient1", "recipient2"])

        expected_twiml = "<Response><Say>Test message</Say></Response>"
        assert mock_twilio_client.calls.create.call_count == 2
        mock_twilio_client.calls.create.assert_any_call(
            to='+12223334444',
            from_='+15556667777',
            twiml=expected_twiml
        )
        mock_twilio_client.calls.create.assert_any_call(
            to='+13334445555',
            from_='+15556667777',
            twiml=expected_twiml
        )

def test_call_invalid_recipient(twilio_client, mock_twilio_client):
    with patch('strideutils.twilio_connector.config') as mock_config:
        mock_config.PHONE_NUMBERS = {}

        with pytest.raises(KeyError):
            twilio_client.call("Test message", "invalid_recipient")

@patch('strideutils.twilio_connector.get_env_or_raise')
def test_twilio_client_initialization(mock_get_env):
    mock_get_env.side_effect = ['fake_account_id', 'fake_api_token', 'fake_alert_numbers']  # just dummy values, so this should fail.

    client = TwilioClient()

    assert client.account_id == 'fake_account_id'
    assert client.api_token == 'fake_api_token'
    assert client.alert_numbers == 'fake_alert_numbers'
    assert isinstance(client.client, TwilioRestClient)
