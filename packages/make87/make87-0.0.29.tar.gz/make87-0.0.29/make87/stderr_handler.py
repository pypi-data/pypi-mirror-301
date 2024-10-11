import sys
import os
import atexit

from make87_messages.text.log_message_pb2 import LogMessage

from .utils import CWD
from .session_manager import SessionManager


class StdErrHandler:
    """Redirects stderr to a topic."""

    def __init__(self, topic):
        self._session_manager = SessionManager.get_instance()
        self._topic = topic
        self._original_stderr = sys.stderr

    def write(self, message):
        if self._topic is not None and message.strip():
            self.publish_log(message)
        self._original_stderr.write(message)

    def flush(self):
        pass

    def publish_log(self, message):
        log_msg = LogMessage()
        log_msg.timestamp.GetCurrentTime()
        log_msg.level = LogMessage.ERROR
        log_msg.message = message
        log_msg.source = "stderr"
        log_msg.file_name = os.path.relpath(__file__, CWD)
        log_msg.line_number = 0
        log_msg.process_id = os.getpid()
        log_msg.thread_id = 0
        self._topic.publish(message=log_msg)

    def restore_stderr(self):
        sys.stderr = self._original_stderr


def setup_stderr_handler(topic_names):
    """Sets up the stderr handler."""
    try:
        topic = SessionManager.get_instance().get_topic(topic_names.STDERR)
        stderr_handler = StdErrHandler(topic)
        sys.stderr = stderr_handler
        atexit.register(stderr_handler.restore_stderr)
    except Exception as e:
        print(f"No stderr topic setup. Will not publish stderr. Error: {e}")


def cleanup_stderr_handler():
    """Cleans up the stderr handler."""
    if isinstance(sys.stderr, StdErrHandler):
        sys.stderr.flush()
        sys.stderr.restore_stderr()
