"""Connections to databases, buckets, and other services."""

import ast

from pydantic_settings import BaseSettings, SettingsConfigDict

from lego.lego_types import OneOrMany


def settings_config(env_prefix: str, **kwargs) -> SettingsConfigDict:
    """Create a configuration for settings model."""
    ## With `extra="ignore"`, we can put many settings in one .env file.
    return SettingsConfigDict(
        env_prefix=env_prefix,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        **kwargs,
    )


class APIKeys:
    """API keys for some service provider."""

    def __init__(self, api_keys: OneOrMany[str]):
        self.api_keys = api_keys if isinstance(api_keys, list) else [api_keys]
        self.api_key = self.api_keys[0]

    @classmethod
    def from_list_string(cls, api_keys: str) -> "APIKeys":
        """Create an APIKeys object from a string representing a list."""
        api_keys = api_keys.strip()
        if api_keys.startswith("[") and api_keys.endswith("]"):
            return APIKeys(ast.literal_eval(api_keys))
        if api_keys.startswith("'") and api_keys.endswith("'"):
            return APIKeys(ast.literal_eval(api_keys))
        raise ValueError(
            "Value is not enclosed with [] or ''."
            "Use for strings the following format: \"'<value>'\""
        )

    def __getitem__(self, idx: int) -> str:
        return self.api_keys[idx % len(self.api_keys)]

    def __len__(self) -> int:
        return len(self.api_keys)


class MilvusConnection(BaseSettings):
    """Settings to establish a connection with MilvusDB."""

    model_config = settings_config("milvus_")

    uri: str
    token: str


class S3Connection(BaseSettings):
    """Settings to establish a connection with an S3 bucket."""

    model_config = settings_config("s3_")

    access_key: str
    secret_key: str


class RedisConnection(BaseSettings):
    """Settings to establish a connection with a Redis database."""

    model_config = settings_config("redis_")

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str | None = None

    def url(self) -> str:
        """Create a URL to connect to the Redis database."""
        url_after_pass = f"{self.host}:{self.port}/{self.db}"
        url = (
            f":{self.password}@{url_after_pass}"
            if self.password
            else url_after_pass
        )
        return f"redis://{url}"
