"""
Unit tests for GetMessagesUseCase.
Tests cover: successful retrieval, pagination, filtering, error handling, and edge cases.
"""
import pytest
from datetime import datetime
from unittest.mock import Mock

from src.Application.use_cases.get_messages_use_case import GetMessagesUseCase
from src.Application.dtos.pagination_dto import PaginationDTO, GetMessagesFilterDTO
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Domain.value_objects.message_metadata import MessageMetadata


class TestGetMessagesUseCaseSuccess:
    """Tests for successful message retrieval."""

    def test_get_messages_returns_paginated_response(self):
        """Should return PaginationDTO with items, limit, offset, and total."""
        # Arrange
        repository = Mock()

        messages = [
            MessageEntity(
                message_id="msg-1",
                session_id="session-abc",
                content="First message",
                timestamp=datetime.now(),
                sender=SenderType.USER,
                metadata=MessageMetadata(word_count=2, character_count=13, processed_at=datetime.now())
            ),
            MessageEntity(
                message_id="msg-2",
                session_id="session-abc",
                content="Second message",
                timestamp=datetime.now(),
                sender=SenderType.SYSTEM,
                metadata=MessageMetadata(word_count=2, character_count=14, processed_at=datetime.now())
            )
        ]

        repository.get_by_session.return_value = messages
        repository.count_by_session.return_value = 2

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=10,
            offset=0,
            sender=None
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        assert result is not None
        assert isinstance(result, PaginationDTO)
        assert isinstance(result.items, list)
        assert len(result.items) == 2
        assert result.limit == 10
        assert result.offset == 0
        assert result.total == 2

    def test_get_messages_with_no_messages_returns_empty_list(self):
        """Should return empty items list when no messages exist for session."""
        # Arrange
        repository = Mock()
        repository.get_by_session.return_value = []
        repository.count_by_session.return_value = 0

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-empty",
            limit=10,
            offset=0
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        assert result.items == []
        assert result.total == 0
        assert result.limit == 10
        assert result.offset == 0

    def test_get_messages_calls_repository_with_correct_params(self):
        """Should call repository with session_id, limit, offset, and sender."""
        # Arrange
        repository = Mock()
        repository.get_by_session.return_value = []
        repository.count_by_session.return_value = 0

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-123",
            limit=20,
            offset=10,
            sender="user"
        )

        # Act
        use_case.execute(filters)

        # Assert
        repository.get_by_session.assert_called_once_with(
            session_id="session-123",
            limit=20,
            offset=10,
            sender="user"
        )


class TestGetMessagesUseCasePagination:
    """Tests for pagination functionality."""

    def test_get_messages_respects_limit_parameter(self):
        """Should respect the limit parameter for pagination."""
        # Arrange
        repository = Mock()
        messages = [
            MessageEntity(
                message_id=f"msg-{i}",
                session_id="session-abc",
                content=f"Message {i}",
                timestamp=datetime.now(),
                sender=SenderType.USER
            )
            for i in range(5)
        ]

        repository.get_by_session.return_value = messages[:3]  # Simulate limit=3
        repository.count_by_session.return_value = 5

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=3,
            offset=0
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        assert len(result.items) == 3
        assert result.limit == 3
        assert result.total == 5

    def test_get_messages_respects_offset_parameter(self):
        """Should respect the offset parameter for pagination."""
        # Arrange
        repository = Mock()
        messages = [
            MessageEntity(
                message_id=f"msg-{i}",
                session_id="session-abc",
                content=f"Message {i}",
                timestamp=datetime.now(),
                sender=SenderType.USER
            )
            for i in range(3, 5)
        ]

        repository.get_by_session.return_value = messages
        repository.count_by_session.return_value = 5

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=10,
            offset=3
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        assert result.offset == 3
        assert result.total == 5

    def test_get_messages_with_max_limit_100(self):
        """Should accept limit of 100 without error."""
        # Arrange
        repository = Mock()
        repository.get_by_session.return_value = []
        repository.count_by_session.return_value = 0

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=100,  # Max limit
            offset=0
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        call_args = repository.get_by_session.call_args
        assert call_args[1]["limit"] == 100


class TestGetMessagesUseCaseFiltering:
    """Tests for message filtering by sender."""

    def test_get_messages_filters_by_user_sender(self):
        """Should filter messages to only 'user' sender when specified."""
        # Arrange
        repository = Mock()
        user_messages = [
            MessageEntity(
                message_id="msg-1",
                session_id="session-abc",
                content="User message",
                timestamp=datetime.now(),
                sender=SenderType.USER
            )
        ]

        repository.get_by_session.return_value = user_messages
        repository.count_by_session.return_value = 1

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=10,
            offset=0,
            sender="user"
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        repository.get_by_session.assert_called_once()
        call_args = repository.get_by_session.call_args
        assert call_args[1]["sender"] == "user"
        assert all(msg.sender == SenderType.USER for msg in result.items)

    def test_get_messages_filters_by_system_sender(self):
        """Should filter messages to only 'system' sender when specified."""
        # Arrange
        repository = Mock()
        system_messages = [
            MessageEntity(
                message_id="msg-2",
                session_id="session-abc",
                content="System message",
                timestamp=datetime.now(),
                sender=SenderType.SYSTEM
            )
        ]

        repository.get_by_session.return_value = system_messages
        repository.count_by_session.return_value = 1

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=10,
            offset=0,
            sender="system"
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        call_args = repository.get_by_session.call_args
        assert call_args[1]["sender"] == "system"
        assert all(msg.sender == SenderType.SYSTEM for msg in result.items)

    def test_get_messages_returns_all_senders_when_no_filter(self):
        """Should return messages from all senders when no sender filter specified."""
        # Arrange
        repository = Mock()
        all_messages = [
            MessageEntity(
                message_id="msg-1",
                session_id="session-abc",
                content="User message",
                timestamp=datetime.now(),
                sender=SenderType.USER
            ),
            MessageEntity(
                message_id="msg-2",
                session_id="session-abc",
                content="System message",
                timestamp=datetime.now(),
                sender=SenderType.SYSTEM
            )
        ]

        repository.get_by_session.return_value = all_messages
        repository.count_by_session.return_value = 2

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=10,
            offset=0,
            sender=None
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        call_args = repository.get_by_session.call_args
        assert call_args[1]["sender"] is None
        assert len(result.items) == 2


class TestGetMessagesUseCaseValidation:
    """Tests for input validation (handled by Pydantic DTO)."""

    def test_get_messages_with_empty_session_id_raises_error(self):
        """Should raise ValueError when session_id is empty."""
        # Arrange
        repository = Mock()
        use_case = GetMessagesUseCase(repository)

        filters = GetMessagesFilterDTO(
            session_id="",
            limit=10,
            offset=0
        )

        # Act & Assert
        with pytest.raises(ValueError, match="session_id cannot be empty"):
            use_case.execute(filters)


class TestGetMessagesUseCaseEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_get_messages_with_limit_1_is_valid(self):
        """Should accept limit of 1 (minimum valid)."""
        # Arrange
        repository = Mock()
        repository.get_by_session.return_value = []
        repository.count_by_session.return_value = 0

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=1,
            offset=0
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        call_args = repository.get_by_session.call_args
        assert call_args[1]["limit"] == 1

    def test_get_messages_ordered_by_timestamp_ascending(self):
        """Should return messages ordered by timestamp ascending."""
        # Arrange
        repository = Mock()

        now = datetime.now()
        messages = [
            MessageEntity(
                message_id="msg-1",
                session_id="session-abc",
                content="First",
                timestamp=now,
                sender=SenderType.USER
            ),
            MessageEntity(
                message_id="msg-2",
                session_id="session-abc",
                content="Second",
                timestamp=now,
                sender=SenderType.SYSTEM
            )
        ]

        repository.get_by_session.return_value = messages
        repository.count_by_session.return_value = 2

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=10,
            offset=0
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        assert len(result.items) == 2
        assert result.items[0].message_id == "msg-1"
        assert result.items[1].message_id == "msg-2"

    def test_get_messages_returns_only_specified_session(self):
        """Should return only messages from the specified session_id."""
        # Arrange
        repository = Mock()
        messages = [
            MessageEntity(
                message_id="msg-1",
                session_id="session-abc",
                content="Message for session-abc",
                timestamp=datetime.now(),
                sender=SenderType.USER
            )
        ]

        repository.get_by_session.return_value = messages
        repository.count_by_session.return_value = 1

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=10,
            offset=0
        )

        # Act
        result = use_case.execute(filters)

        # Assert
        repository.get_by_session.assert_called_once()
        call_args = repository.get_by_session.call_args
        assert call_args[1]["session_id"] == "session-abc"
        assert all(msg.session_id == "session-abc" for msg in result.items)


