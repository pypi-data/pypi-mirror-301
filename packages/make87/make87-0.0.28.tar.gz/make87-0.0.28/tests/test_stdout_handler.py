# tests/test_stdout_handler.py

from unittest.mock import MagicMock
import sys

from make87.stdout_handler import StdOutHandler


def test_stdout_handler():
    mock_topic = MagicMock()

    original_stdout = sys.stdout

    stdout_handler = StdOutHandler(topic=mock_topic)
    assert stdout_handler._topic is not None

    sys.stdout = stdout_handler

    # Write to stdout
    print("Test stdout message")

    # Restore stdout
    stdout_handler.restore_stdout()

    # Verify that publish was called
    mock_topic.publish.assert_called()
    calls = mock_topic.publish.call_args_list
    assert any("Test stdout message" in kwargs["message"].message for args, kwargs in calls)

    # Ensure original stdout is restored
    assert sys.stdout == original_stdout
