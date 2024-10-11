import pytest
from unittest.mock import patch, MagicMock

from make87.session_manager import SessionManager
from make87.messages import PUB, reset_sockets_cache, reset_peripherals_cache


@pytest.fixture(autouse=True)
def reset_caches():
    reset_sockets_cache()
    reset_peripherals_cache()


@patch("zenoh.open")
@patch("make87.session_manager.parse_sockets")
def test_initialize_session(mock_parse_sockets, mock_zenoh_open):
    # Mocking the sockets
    mock_socket = MagicMock(spec=PUB)
    mock_socket.topic_key = "test_topic_key"
    mock_socket.socket_type = "PUB"
    mock_socket.message_type = "make87_messages.datetime.timestamp.TimeStamp"

    mock_sockets = MagicMock()
    mock_sockets.sockets = [mock_socket]
    mock_parse_sockets.return_value = mock_sockets

    # Mocking the Zenoh session
    mock_session = MagicMock()
    mock_zenoh_open.return_value = mock_session

    session_manager = SessionManager.get_instance()
    session_manager.initialize()

    assert session_manager.get_session() is not None
    assert "test_topic_key" in session_manager._topics


@patch("zenoh.open")
@patch("make87.messages.parse_sockets")
def test_get_topic(mock_parse_sockets, mock_zenoh_open):
    # Setup similar to previous test
    mock_socket = MagicMock()
    mock_socket.topic_key = "test_topic_key"
    mock_socket.socket_type = "PUB"
    mock_socket.message_type = "make87_messages.datetime.timestamp.TimeStamp"

    mock_sockets = MagicMock()
    mock_sockets.sockets = [mock_socket]
    mock_parse_sockets.return_value = mock_sockets

    mock_session = MagicMock()
    mock_zenoh_open.return_value = mock_session

    session_manager = SessionManager.get_instance()
    session_manager.initialize()
    topic = session_manager.get_topic("test_topic_key")
    assert topic is not None


@patch("zenoh.open")
@patch("make87.messages.parse_sockets")
def test_get_topic_not_found(mock_parse_sockets, mock_zenoh_open):
    mock_sockets = MagicMock()
    mock_sockets.sockets = []
    mock_parse_sockets.return_value = mock_sockets

    session_manager = SessionManager.get_instance()
    session_manager.initialize()
    with pytest.raises(ValueError):
        session_manager.get_topic("unknown_topic_key")
