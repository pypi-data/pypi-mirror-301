# tests/test_stderr_handler.py

from unittest.mock import MagicMock
import sys

from make87.stderr_handler import StdErrHandler


def test_stderr_handler():
    mock_topic = MagicMock()

    original_stderr = sys.stderr

    stderr_handler = StdErrHandler(topic=mock_topic)
    assert stderr_handler._topic is not None

    sys.stderr = stderr_handler

    # Write to stderr
    print("Test stderr message", file=sys.stderr)

    # Restore stderr
    stderr_handler.restore_stderr()

    # Verify that publish was called
    mock_topic.publish.assert_called()
    calls = mock_topic.publish.call_args_list
    assert any("Test stderr message" in kwargs["message"].message for args, kwargs in calls)

    # Ensure original stderr is restored
    assert sys.stderr == original_stderr
