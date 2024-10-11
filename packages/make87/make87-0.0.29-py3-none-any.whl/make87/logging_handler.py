import logging
import os
from datetime import datetime, timezone

from make87_messages.text.log_message_pb2 import LogMessage

from make87.utils import LEVEL_MAPPING, CWD
from make87.session_manager import SessionManager


class LogHandler(logging.Handler):
    """Custom logging handler that publishes logs to a topic."""

    def __init__(self, topic):
        super().__init__()
        self._session_manager = SessionManager.get_instance()
        self._topic = topic

    def emit(self, record):
        if self._topic is None:
            return

        log_msg = LogMessage()
        log_msg.timestamp.FromDatetime(datetime.fromtimestamp(record.created, tz=timezone.utc))
        log_msg.level = LEVEL_MAPPING.get(record.levelname, LogMessage.INFO)
        log_msg.message = record.getMessage()
        log_msg.source = record.name
        log_msg.file_name = os.path.relpath(record.pathname, CWD)
        log_msg.line_number = record.lineno
        log_msg.process_id = record.process
        log_msg.thread_id = record.thread
        self._topic.publish(message=log_msg)


def setup_logging(topic_names):
    """Sets up the logging handler."""
    logger = logging.getLogger()
    try:
        topic = SessionManager.get_instance().get_topic(topic_names.LOGS)
        log_handler = LogHandler(topic)
        logger.addHandler(log_handler)
    except Exception as e:
        print(f"No log topic setup. Will not publish logs. Error: {e}")


def cleanup_logging():
    """Cleans up the logging handler."""
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        if isinstance(handler, LogHandler):
            handler.flush()
            handler.close()
            logger.removeHandler(handler)
