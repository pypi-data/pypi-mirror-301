# tests/test_topics.py

from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from make87.topics import PublisherTopic, SubscriberTopic, MultiSubscriberTopic
from make87.messages import MessageMetadata


@patch("make87.topics._import_class_from_string")
def test_publisher_topic(mock_import_class):
    mock_message_class = MagicMock()
    mock_message_instance = MagicMock()
    mock_message_instance.HasField.return_value = False
    mock_message_instance.timestamp = MagicMock()
    mock_message_instance.SerializeToString.return_value = b"serialized_message"
    mock_message_class.return_value = mock_message_instance
    mock_import_class.return_value = mock_message_class

    mock_session = MagicMock()
    mock_publisher = MagicMock()
    mock_session.declare_publisher.return_value = mock_publisher

    publisher_topic = PublisherTopic("test_topic", "make87_messages.datetime.timestamp.TimeStamp", mock_session)
    publisher_topic.publish(mock_message_instance)

    mock_publisher.put.assert_called_once_with(b"serialized_message")


@patch("make87.topics._import_class_from_string")
def test_subscriber_topic(mock_import_class):
    mock_message_class = MagicMock()
    mock_message_instance = MagicMock()
    mock_message_class.return_value = mock_message_instance
    mock_import_class.return_value = mock_message_class

    mock_session = MagicMock()
    mock_subscriber = MagicMock()
    mock_session.declare_subscriber.return_value = mock_subscriber

    subscriber_topic = SubscriberTopic("test_topic", "make87_messages.datetime.timestamp.TimeStamp", mock_session)

    def test_callback(message, metadata):
        assert message == mock_message_instance
        assert isinstance(metadata, MessageMetadata)
        assert metadata.topic_name == "test_topic"

    subscriber_topic.subscribe(test_callback)
    assert len(subscriber_topic._subscribers) == 1

    # Simulate receiving a message
    sample = MagicMock()
    sample.payload = b"serialized_message"
    sample.key_expr = "test_topic"

    subscriber_topic.decode_message(sample, callback=test_callback)


@patch("make87.topics.SubscriberTopic")
def test_multi_subscriber_topic(mock_subscriber_topic_class):
    # Mock two SubscriberTopic instances
    mock_subscriber_topic1 = MagicMock()
    mock_subscriber_topic1.name = "topic1"
    mock_subscriber_topic2 = MagicMock()
    mock_subscriber_topic2.name = "topic2"

    # Instantiate MultiSubscriberTopic
    multi_subscriber = MultiSubscriberTopic(
        topics=[mock_subscriber_topic1, mock_subscriber_topic2], delta=0.1, max_queue_size=10
    )

    # Mock messages
    message1 = MagicMock()
    message1.timestamp.ToDatetime.return_value = datetime.now(timezone.utc)
    message2 = MagicMock()
    message2.timestamp.ToDatetime.return_value = datetime.now(timezone.utc)

    metadata1 = MessageMetadata(topic_name="topic1", topic_key="key1")
    metadata2 = MessageMetadata(topic_name="topic2", topic_key="key2")

    # Define callback
    def test_callback(messages, metadatas):
        assert len(messages) == 2
        assert len(metadatas) == 2

    multi_subscriber.subscribe(test_callback)

    # Simulate receiving messages
    multi_subscriber._buffer_message(message1, metadata1)
    multi_subscriber._buffer_message(message2, metadata2)
