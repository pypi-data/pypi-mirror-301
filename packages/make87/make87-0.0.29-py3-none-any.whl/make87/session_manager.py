import zenoh
import threading
import json
import os
from typing import Optional

from make87.messages import PUB, SUB, parse_sockets
from make87.topics import PublisherTopic, SubscriberTopic


class SessionManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._session: Optional[zenoh.Session] = None
        self._topics = {}
        self._initialized = False

    @classmethod
    def get_instance(cls):
        """Singleton pattern to ensure only one instance exists."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def initialize(self):
        """Initialize the session and topics."""
        with self._lock:
            if self._initialized:
                return  # Already initialized

            # Read configuration from environment variables
            config = None
            if "COMM_CONFIG" in os.environ:
                config = json.loads(os.environ["COMM_CONFIG"])
                config = zenoh.Config.from_obj(config)
            self._session = zenoh.open(config=config)
            # Initialize topics
            self._initialize_topics()
            self._initialized = True

    def _initialize_topics(self):
        """Initialize topics based on the SOCKETS environment variable."""
        socket_data = parse_sockets()
        for socket in socket_data.sockets:
            if socket.topic_key in self._topics:
                continue  # Topic already initialized
            if isinstance(socket, PUB):
                topic = PublisherTopic(
                    name=socket.topic_key,
                    message_type=socket.message_type,
                    session=self._session,
                )
            elif isinstance(socket, SUB):
                topic = SubscriberTopic(
                    name=socket.topic_key,
                    message_type=socket.message_type,
                    session=self._session,
                )
            else:
                raise ValueError(f"Invalid socket type {socket.socket_type}")
            self._topics[socket.topic_key] = topic

    def get_session(self):
        """Retrieve the Zenoh session. Must be called after initialization."""
        if not self._initialized:
            raise RuntimeError("SessionManager not initialized. Call initialize() first.")
        return self._session

    def get_topic(self, name):
        """Retrieve a topic by name. Must be called after initialization."""
        if not self._initialized:
            raise RuntimeError("SessionManager not initialized. Call initialize() first.")
        if name not in self._topics:
            available_topics = ", ".join(self._topics.keys())
            raise ValueError(f"Topic '{name}' not found. Available topics: {available_topics}")
        return self._topics[name]

    def close(self):
        """Clean up the session and topics."""
        with self._lock:
            if self._session:
                self._session.close()
                self._session = None
                self._topics = {}
                self._initialized = False


# Expose the initialize function
def initialize():
    session_manager = SessionManager.get_instance()
    session_manager.initialize()
