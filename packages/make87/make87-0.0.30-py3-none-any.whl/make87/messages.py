from dataclasses import dataclass
from typing import List, Union, Literal, Annotated
from threading import Lock
import os
import json

from pydantic import BaseModel, Field


class PUB(BaseModel):
    socket_type: Literal["PUB"]
    topic_name: str
    topic_key: str
    message_type: str


class SUB(BaseModel):
    socket_type: Literal["SUB"]
    topic_name: str
    topic_key: str
    message_type: str


Socket = Annotated[Union[PUB, SUB], Field(discriminator="socket_type")]


class Sockets(BaseModel):
    sockets: List[Socket]


class Peripheral(BaseModel):
    name: str
    mount: Union[str, int]


class Peripherals(BaseModel):
    peripherals: List[Peripheral]


@dataclass
class MessageMetadata:
    topic_name: str
    topic_key: str


# Parsing functions and caches
_sockets_cache = None
_sockets_cache_lock = Lock()

_peripherals_cache = None
_peripherals_cache_lock = Lock()


def parse_sockets():
    global _sockets_cache
    with _sockets_cache_lock:
        if _sockets_cache is None:
            try:
                socket_data_env = os.environ["SOCKETS"]
                socket_data = Sockets.model_validate_json(socket_data_env)
                _sockets_cache = socket_data
            except KeyError:
                raise EnvironmentError("`SOCKETS` environment variable not set.")
            except json.JSONDecodeError as e:
                raise ValueError("`SOCKETS` environment variable is not valid JSON.") from e
        return _sockets_cache


def parse_peripherals():
    global _peripherals_cache
    with _peripherals_cache_lock:
        if _peripherals_cache is None:
            try:
                peripheral_data_env = os.environ.get("PERIPHERALS", '{"peripherals":[]}')
                peripheral_data = Peripherals.model_validate_json(peripheral_data_env)
                _peripherals_cache = peripheral_data
            except json.JSONDecodeError:
                raise ValueError("`PERIPHERALS` environment variable is not valid JSON.")
        return _peripherals_cache


def reset_sockets_cache():
    global _sockets_cache
    with _sockets_cache_lock:
        _sockets_cache = None


def reset_peripherals_cache():
    global _peripherals_cache
    with _peripherals_cache_lock:
        _peripherals_cache = None
