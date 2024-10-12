from _typeshed import Incomplete
from strideutils.stride_config import config as config
from typing import Iterable, Union, List

_: Incomplete
CALL_TEMPLATE: str
client: Incomplete

def send_calls(msg: str, to: Union[str, Iterable[str], List[str]]) -> None: ...

class TwilioClient:
    _instance: 'TwilioClient'
    call_template: str
    account_id: str
    api_token: str
    alert_numbers: str
    client: Incomplete

    def __new__(cls) -> 'TwilioClient': ...
    def __init__(self) -> None: ...
    def call(self, msg: str, to: Union[str, Iterable[str], List[str]]) -> None: ...
