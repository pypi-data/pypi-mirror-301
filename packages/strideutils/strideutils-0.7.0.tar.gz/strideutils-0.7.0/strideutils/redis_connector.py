"""
Redis Connector for Stride Utils

This module provides a singleton client for interacting with all the Redis databases
used in Stride. Uses stride_config to connect to different Redis instances
(public, frontend, backend, etc.) and provides methods for common Redis operations
like get, set, and scan.
"""

from typing import Dict, List, Optional

import redis

from strideutils.stride_config import Environment as e
from strideutils.stride_config import get_env_or_raise

DATABASE_ENVIRONMENT_CONFIGS = {
    'public': (e.UPSTASH_PUBLIC_HOST, e.UPSTASH_PUBLIC_PORT, e.UPSTASH_PUBLIC_PASSWORD),
    'frontend': (e.UPSTASH_FRONTEND_HOST, e.UPSTASH_FRONTEND_PORT, e.UPSTASH_FRONTEND_PASSWORD),
    'backend': (e.UPSTASH_BACKEND_HOST, e.UPSTASH_BACKEND_PORT, e.UPSTASH_BACKEND_PASSWORD),
    'dydx': (e.UPSTASH_DYDX_HOST, e.UPSTASH_DYDX_PORT, e.UPSTASH_DYDX_PASSWORD),
    'dydx_airdrop': (e.UPSTASH_DYDX_AIRDROP_HOST, e.UPSTASH_DYDX_AIRDROP_PORT, e.UPSTASH_DYDX_AIRDROP_PASSWORD),
    'saga_airdrop': (e.UPSTASH_SAGA_AIRDROP_HOST, e.UPSTASH_SAGA_AIRDROP_PORT, e.UPSTASH_SAGA_AIRDROP_PASSWORD),
    'milestones': (e.UPSTASH_MILESTONES_HOST, e.UPSTASH_MILESTONES_PORT, e.UPSTASH_MILESTONES_PASSWORD),
}
ALL_DATABASE_NAMES = list(DATABASE_ENVIRONMENT_CONFIGS.keys())


class RedisClient:
    """Singleton client used to interact with Redis databases."""

    _instance = None
    _dbs: Dict[str, redis.Redis] = {}

    def __new__(cls, db_names: Optional[List[str]] = None):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.__init__(db_names)
        return cls._instance

    def __init__(self, db_names: Optional[List[str]] = None):
        if len(self._dbs) == 0:
            self._init_dbs(db_names)

    def _init_dbs(self, db_names: Optional[List[str]] = None):
        """
        Initializes Redis database connections.

        Args:
            db_names: Optional list of database names to initialize. If None, initializes all databases.

        Raises:
            ValueError: If db_names is an empty list or contains invalid database names.
        """
        if db_names is not None and len(db_names) == 0:
            raise ValueError("db_names cannot be an empty list")

        db_names = db_names or ALL_DATABASE_NAMES
        invalid_db_names = [name for name in db_names if name not in ALL_DATABASE_NAMES]
        if invalid_db_names:
            raise ValueError(f"Invalid Redis database names: {invalid_db_names}")

        for name in db_names:
            if name not in self._dbs:
                self._dbs[name] = self._init_db(name)

    @staticmethod
    def _init_db(database_name: str) -> redis.Redis:
        """
        Initializes a database connection by checking that the proper environment variables
        are specified and saving the database in the client.

        Args:
            database_name: Name of the database to initialize.

        Returns:
            redis.Redis: Initialized Redis client.
        """
        host_env, port_env, password_env = DATABASE_ENVIRONMENT_CONFIGS[database_name]
        db_config = {
            'host': get_env_or_raise(host_env),
            'port': int(get_env_or_raise(port_env)),
            'password': get_env_or_raise(password_env),
            'ssl': True,
            'decode_responses': True,
        }
        return redis.Redis(**db_config)

    def get_db(self, name: Optional[str] = None) -> redis.Redis:
        """
        Returns the Redis db specified by name.
        If name is None, returns the only configured database or raises an error if multiple are configured.

        Args:
            name: Optional name of the database to retrieve.

        Returns:
            redis.Redis: The requested Redis database client.

        Raises:
            ValueError: If no name is provided and multiple databases are configured,
                        or if the requested database name has not been configured.
        """
        if name is None:
            if len(self._dbs) != 1:
                raise ValueError("Database name must be specified if multiple databases are configured")
            return next(iter(self._dbs.values()))

        if name not in self._dbs:
            raise ValueError(f"Database {name} has not been configured.")
        return self._dbs[name]

    def get(self, key: str, db_name: Optional[str] = None) -> Optional[str]:
        """
        Reads the given Redis key and returns the value.

        Args:
            key: The key to retrieve.
            db_name: Optional name of the database to use.

        Returns:
            Optional[str]: The value associated with the key, or None if the key doesn't exist.
        """
        db = self.get_db(db_name)
        return db.get(key)

    def get_multiple_keys(self, keys: List[str], db_name: Optional[str] = None) -> List[Optional[str]]:
        """
        Reads multiple keys at once.

        Args:
            keys: List of keys to retrieve.
            db_name: Optional name of the database to use.

        Returns:
            List[Optional[str]]: List of values associated with the keys.
        """
        db = self.get_db(db_name)
        return db.mget(keys)

    def get_all_keys(self, db_name: Optional[str] = None) -> List[str]:
        """
        Returns all keys in the specified Redis db.

        Args:
            db_name: Optional name of the database to use.

        Returns:
            List[str]: List of all keys in the database.
        """
        db = self.get_db(db_name)
        keys = []
        cursor = 0
        while True:
            cursor, partial_keys = db.scan(cursor, count=1000)
            keys.extend(partial_keys)
            if cursor == 0:
                break
        return keys

    def set(self, key: str, val: str, db_name: Optional[str] = None) -> None:
        """
        Sets the given key to value in the specified Redis db.

        Args:
            key: The key to set.
            val: The value to set.
            db_name: Optional name of the database to use.
        """
        db = self.get_db(db_name)
        db.set(key, val)

    def set_keys(self, dict_to_upload: Dict[str, str], db_name: Optional[str] = None, prefix: str = '') -> None:
        """
        Sets multiple keys and values in the Redis db.

        Args:
            dict_to_upload: Dictionary of key-value pairs to set.
            db_name: Optional name of the database to use.
            prefix: Optional prefix to add to all keys.
        """
        db = self.get_db(db_name)
        with db.pipeline() as pipe:
            for k, v in dict_to_upload.items():
                pipe.set(prefix + k, v)
            pipe.execute()

    @classmethod
    def _reset(cls):
        """
        Resets the RedisClient singleton instance and clears all database connections.
        This method is private and is primarily used for testing purposes.
        """
        cls._instance = None
        cls._dbs.clear()
