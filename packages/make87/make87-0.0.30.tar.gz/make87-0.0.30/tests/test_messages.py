import pytest
from unittest.mock import patch
import os

from make87.messages import PUB, SUB, Sockets, Peripherals, parse_sockets, parse_peripherals
from make87.messages import reset_sockets_cache, reset_peripherals_cache


@pytest.fixture(autouse=True)
def reset_caches():
    reset_sockets_cache()
    reset_peripherals_cache()


def test_pub_model():
    pub = PUB(
        socket_type="PUB",
        topic_name="TestTopic",
        topic_key="test_topic_key",
        message_type="make87_messages.datetime.timestamp.TimeStamp",
    )
    assert pub.socket_type == "PUB"
    assert pub.topic_name == "TestTopic"
    assert pub.message_type == "make87_messages.datetime.timestamp.TimeStamp"


def test_sub_model():
    sub = SUB(
        socket_type="SUB",
        topic_name="TestTopic",
        topic_key="test_topic_key",
        message_type="make87_messages.datetime.timestamp.TimeStamp",
    )
    assert sub.socket_type == "SUB"
    assert sub.topic_name == "TestTopic"
    assert sub.message_type == "make87_messages.datetime.timestamp.TimeStamp"


@patch.dict(
    os.environ,
    {
        "SOCKETS": '{"sockets": [{"socket_type": "PUB", "topic_name": "TestTopic", "topic_key": "test_topic_key", "message_type": "make87_messages.datetime.timestamp.TimeStamp"}]}'
    },
)
def test_parse_sockets():
    sockets = parse_sockets()
    assert isinstance(sockets, Sockets)
    assert len(sockets.sockets) == 1
    assert sockets.sockets[0].socket_type == "PUB"
    assert sockets.sockets[0].topic_name == "TestTopic"


@patch.dict(os.environ, {"PERIPHERALS": '{"peripherals": [{"name": "Camera", "mount": "/dev/video0"}]}'})
def test_parse_peripherals():
    peripherals = parse_peripherals()
    assert isinstance(peripherals, Peripherals)
    assert len(peripherals.peripherals) == 1
    assert peripherals.peripherals[0].name == "Camera"
    assert peripherals.peripherals[0].mount == "/dev/video0"


@patch.dict(os.environ, {})
def test_parse_sockets_env_not_set():
    with pytest.raises(EnvironmentError):
        parse_sockets()


@patch.dict(os.environ, {"SOCKETS": "invalid_json"})
def test_parse_sockets_invalid_json():
    with pytest.raises(ValueError):
        parse_sockets()


@patch.dict(os.environ, {"PERIPHERALS": "invalid_json"})
def test_parse_peripherals_invalid_json():
    with pytest.raises(ValueError):
        parse_peripherals()
