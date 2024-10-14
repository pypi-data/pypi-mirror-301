import tomllib
from enum import Enum
from typing import Annotated, Optional, Self, List, Any, Dict
from pydantic import BaseModel, Field
from pydantic.functional_validators import AfterValidator
from datetime import timedelta
from ashtree.util import LogLevelName, convert_log_level
from mongey.types import CacheEngineName


_DEFAULT_TIMEOUT = timedelta(seconds=1, milliseconds=100)
_DEFAULT_COOKIE_TTL = timedelta(days=90)


class SessionConfig(BaseModel):
    cookie: str = "_ashtree_session_id"
    ttl: timedelta = _DEFAULT_COOKIE_TTL


class DatabaseConfig(BaseModel):
    uri: str = "mongodb://localhost:27017/test"
    timeout: timedelta = _DEFAULT_TIMEOUT


class LogConfig(BaseModel):
    level: Annotated[LogLevelName, AfterValidator(convert_log_level)] = 10


class CacheConfig(BaseModel):
    level1: "CacheEngineName" = "request_local"
    level2: "CacheEngineName" = "memcached"
    level1_options: Optional[Dict[str, Any]] = None
    level2_options: Optional[Dict[str, Any]] = Field(default_factory=lambda: {"backends": ["127.0.0.1:11211"]})


class JWTConfig(BaseModel):
    enabled: bool = False
    secret_key: Optional[str] = None


class TaskConfig(BaseModel):
    redis_url: str = "redis://127.0.0.1:6379/0"
    queue: str = "default"


class BaseConfig(BaseModel):
    session: SessionConfig = Field(default_factory=SessionConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    logging: LogConfig = Field(default_factory=LogConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    jwt: JWTConfig = Field(default_factory=JWTConfig)
    tasks: TaskConfig = Field(default_factory=TaskConfig)

    @classmethod
    def parse(cls, filename) -> Self:
        with open(filename, "rb") as f:
            config = tomllib.load(f)
        return cls(**config)

    def get(self, key: str) -> Any:
        tokens = key.split(".")
        node = self
        while tokens:
            token = tokens.pop(0)
            try:
                node = getattr(node, token)
            except AttributeError:
                raise KeyError(f"key {key} does not exist")
        return node
