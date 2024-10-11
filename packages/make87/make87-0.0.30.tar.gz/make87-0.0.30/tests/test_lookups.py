# tests/test_lookups.py

import pytest
from unittest.mock import patch
import os

from make87.lookups import TopicNamesLookup, PeripheralNamesLookup
from make87.messages import reset_sockets_cache, reset_peripherals_cache


@pytest.fixture(autouse=True)
def reset_caches():
    reset_sockets_cache()
    reset_peripherals_cache()


@patch.dict(
    os.environ,
    {
        "SOCKETS": '{"sockets": [{"socket_type": "PUB", "topic_name": "TestTopic", "topic_key": "test_topic_key", "message_type": "make87_messages.datetime.timestamp.TimeStamp"}]}'
    },
)
def test_topic_names_lookup():
    topic_names = TopicNamesLookup()
    topic_names.initialize()
    assert topic_names.TestTopic == "test_topic_key"
    with pytest.raises(AttributeError):
        _ = topic_names.UnknownTopic


@patch.dict(os.environ, {"PERIPHERALS": '{"peripherals": [{"name": "Camera", "mount": "/dev/video0"}]}'})
def test_peripheral_names_lookup():
    peripheral_names = PeripheralNamesLookup()
    peripheral_names.initialize()
    assert peripheral_names.Camera == "/dev/video0"
    with pytest.raises(AttributeError):
        _ = peripheral_names.UnknownPeripheral


@patch.dict(os.environ, {})
def test_topic_names_lookup_env_not_set():
    topic_names = TopicNamesLookup()
    with pytest.raises(EnvironmentError):
        topic_names.initialize()


@patch.dict(os.environ, {"SOCKETS": "invalid_json"})
def test_topic_names_lookup_invalid_json():
    topic_names = TopicNamesLookup()
    with pytest.raises(ValueError):
        topic_names.initialize()
