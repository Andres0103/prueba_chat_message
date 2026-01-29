"""
Unit tests for MessageEntity domain entity.
"""
import pytest
from datetime import datetime
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Domain.value_objects.message_metadata import MessageMetadata


class TestMessageEntity:
    """Tests for MessageEntity domain entity."""
    
    def test_create_valid_message_entity(self):
        """Test creating a valid message entity."""
        timestamp = datetime.utcnow()
        message = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="Hello world",
            timestamp=timestamp,
            sender=SenderType.USER
        )
        
        assert message.message_id == "msg-123"
        assert message.session_id == "session-abc"
        assert message.content == "Hello world"
        assert message.timestamp == timestamp
        assert message.sender == SenderType.USER
    
    def test_message_entity_validates_empty_message_id(self):
        """Test that empty message_id raises ValueError."""
        with pytest.raises(ValueError, match="message_id cannot be empty"):
            MessageEntity(
                message_id="",
                session_id="session-abc",
                content="Hello",
                timestamp=datetime.utcnow(),
                sender=SenderType.USER
            )
    
    def test_message_entity_validates_empty_session_id(self):
        """Test that empty session_id raises ValueError."""
        with pytest.raises(ValueError, match="session_id cannot be empty"):
            MessageEntity(
                message_id="msg-123",
                session_id="",
                content="Hello",
                timestamp=datetime.utcnow(),
                sender=SenderType.USER
            )
    
    def test_message_entity_validates_empty_content(self):
        """Test that empty content raises ValueError."""
        with pytest.raises(ValueError, match="content cannot be empty"):
            MessageEntity(
                message_id="msg-123",
                session_id="session-abc",
                content="",
                timestamp=datetime.utcnow(),
                sender=SenderType.USER
            )
    
    def test_with_metadata_returns_new_instance(self):
        """Test that with_metadata returns a new instance with metadata."""
        message = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="Hello world",
            timestamp=datetime.utcnow(),
            sender=SenderType.USER
        )
        
        metadata = MessageMetadata.from_content("Hello world")
        message_with_metadata = message.with_metadata(metadata)
        
        assert message_with_metadata.metadata is not None
        assert message_with_metadata.metadata.word_count == 2
        assert message.metadata is None  # Original remains unchanged
    
    def test_is_from_user_property(self):
        """Test is_from_user property."""
        message = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="Hello",
            timestamp=datetime.utcnow(),
            sender=SenderType.USER
        )
        
        assert message.is_from_user is True
        assert message.is_from_system is False
    
    def test_is_from_system_property(self):
        """Test is_from_system property."""
        message = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="Hello",
            timestamp=datetime.utcnow(),
            sender=SenderType.SYSTEM
        )
        
        assert message.is_from_system is True
        assert message.is_from_user is False