from make87.session_manager import SessionManager  # noqa: F401
from make87.topics import PublisherTopic, SubscriberTopic, MultiSubscriberTopic  # noqa: F401
from make87.messages import PUB, SUB, Socket, Sockets, Peripheral, Peripherals, MessageMetadata  # noqa: F401
from make87.lookups import TopicNamesLookup, PeripheralNamesLookup  # noqa: F401
from make87.logging_handler import setup_logging  # noqa: F401
from make87.stdout_handler import setup_stdout_handler  # noqa: F401
from make87.stderr_handler import setup_stderr_handler  # noqa: F401

# Expose topic names and peripheral names
topic_names = TopicNamesLookup()
peripheral_names = PeripheralNamesLookup()

# Initialize SessionManager instance (not the session itself)
session_manager = SessionManager.get_instance()


def initialize():
    """Initialize the SDK, setting up the session, topics, lookups, and handlers."""
    # Initialize the session manager
    session_manager.initialize()
    # Initialize topic names and peripheral names
    topic_names.initialize()
    peripheral_names.initialize()
    # Set up logging and handlers
    setup_logging(topic_names)
    setup_stdout_handler(topic_names)
    setup_stderr_handler(topic_names)


def get_topic(name: str):
    """Retrieve a topic by name, after the session has been initialized."""
    return session_manager.get_topic(name)
