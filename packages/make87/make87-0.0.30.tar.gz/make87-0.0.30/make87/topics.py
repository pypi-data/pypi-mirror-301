from datetime import timedelta
from functools import partial
from threading import Lock
from typing import List, Callable, Dict, Tuple, Type, Optional
from collections import deque

import zenoh
from google.protobuf.message import Message

from make87.messages import MessageMetadata
from make87.utils import _import_class_from_string


class Topic:
    """Base class for topics."""

    def __init__(self, name: str):
        self.name = name


class PublisherTopic(Topic):
    """Represents a publisher topic."""

    def __init__(self, name: str, message_type: str, session: zenoh.Session):
        super().__init__(name)
        self._session = session
        self._message_type: Type[Message] = _import_class_from_string(message_type)
        self._pub = self._session.declare_publisher(f"{name}")

    @property
    def message_type(self) -> Type[Message]:
        return self._message_type

    def publish(self, message: Message) -> None:
        if not message.HasField("timestamp"):
            message.timestamp.GetCurrentTime()
        self._pub.put(message.SerializeToString())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._pub.undeclare()


class SubscriberTopic(Topic):
    """Represents a subscriber topic."""

    def __init__(self, name: str, message_type: str, session: zenoh.Session):
        super().__init__(name)
        self._subscribers = []
        self._message_type: Type[Message] = _import_class_from_string(message_type)
        self._session = session

    def decode_message(self, sample, callback: Callable):
        message = self._message_type()
        message.ParseFromString(sample.payload)
        callback(message, MessageMetadata(topic_name=self.name, topic_key=str(sample.key_expr)))

    def subscribe(self, callback: Callable) -> None:
        retrieve_callback = partial(self.decode_message, callback=callback)
        sub = self._session.declare_subscriber(f"{self.name}", retrieve_callback)
        self._subscribers.append(sub)

    def close(self):
        for sub in self._subscribers:
            sub.undeclare()
        self._subscribers.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class MultiSubscriberTopic:
    """Handles synchronized subscription to multiple topics."""

    def __init__(
        self,
        topics: List[SubscriberTopic],
        delta: float = 0.1,
        max_queue_size: int = 10,
    ):
        self._subscriber_topics: List[SubscriberTopic] = topics
        self._buffers: Dict[str, deque] = {topic.name: deque(maxlen=max_queue_size) for topic in topics}
        self._delta: timedelta = timedelta(seconds=delta)
        self._lock: Lock = Lock()
        self._callback: Optional[Callable] = None
        self._subscriptions = []

    def _buffer_message(self, message: Message, metadata: MessageMetadata):
        with self._lock:
            self._buffers[metadata.topic_name].append(
                {"message": message, "metadata": metadata, "timestamp": message.timestamp.ToDatetime()}
            )
            self._try_match_messages()

    def _try_match_messages(self):
        while all(self._buffers[topic.name] for topic in self._subscriber_topics):
            msg_group = [self._buffers[topic.name][0] for topic in self._subscriber_topics]
            timestamps = [msg["timestamp"] for msg in msg_group]
            if max(timestamps) - min(timestamps) <= self._delta:
                if self._callback:
                    messages = tuple(msg["message"] for msg in msg_group)
                    metadatas = tuple(msg["metadata"] for msg in msg_group)
                    self._callback(messages, metadatas)
                for topic in self._subscriber_topics:
                    self._buffers[topic.name].popleft()
                return
            else:
                # Remove the oldest message
                oldest_topic_name = min(self._buffers, key=lambda name: self._buffers[name][0]["timestamp"])
                self._buffers[oldest_topic_name].popleft()

    def subscribe(self, callback: Callable[[Tuple[Message, ...], Tuple[MessageMetadata, ...]], None]) -> None:
        self._callback = callback
        for topic in self._subscriber_topics:
            sub = topic.subscribe(self._buffer_message)
            self._subscriptions.append(sub)

    def close(self):
        for topic in self._subscriber_topics:
            topic.close()
        self._subscriptions.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
