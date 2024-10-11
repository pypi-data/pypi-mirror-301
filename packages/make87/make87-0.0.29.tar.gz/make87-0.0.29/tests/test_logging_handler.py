# tests/test_logging_handlers.py

from unittest.mock import MagicMock
import logging

from make87.logging_handler import LogHandler
from make87_messages.text.log_message_pb2 import LogMessage


def test_log_handler_emit():
    mock_topic = MagicMock()

    log_handler = LogHandler(topic=mock_topic)
    assert log_handler._topic is not None

    # Create a log record
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test log message",
        args=None,
        exc_info=None,
    )

    # Emit the log record
    log_handler.emit(record)

    # Verify that publish was called
    mock_topic.publish.assert_called_once()
    args, kwargs = mock_topic.publish.call_args
    assert isinstance(kwargs["message"], LogMessage)
    assert kwargs["message"].message == "Test log message"
