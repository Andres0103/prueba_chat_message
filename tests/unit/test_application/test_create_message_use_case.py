#Test para la creación de mensajes en la aplicación
import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock

from src.Application.use_cases.create_message_use_case import CreateMessageUseCase
from src.Application.dtos.message_dto import CreateMessageDTO, MessageResponseDTO
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Domain.value_objects.message_metadata import MessageMetadata

#Test para la creación de mensajes en la aplicación
class TestCreateMessageUseCaseSuccess:

    #Debe crear un mensaje con datos válidos y devolver MessageResponseDTO
    def test_create_message_with_valid_data_returns_response_dto(self):
        # Arrange, prepare los mocks y datos de prueba
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        test_timestamp = datetime(2026, 1, 30, 10, 0, 0)
        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="Hello world",
            timestamp=test_timestamp,
            sender="user"
        )

        # Act, configura los mocks para devolver valores esperados
        content_filter.filter.return_value = "Hello world"

        saved_entity = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="Hello world",
            timestamp=test_timestamp,
            sender=SenderType.USER,
            metadata=MessageMetadata(
                word_count=2,
                character_count=11,
                processed_at=test_timestamp
            )
        )

        message_processor.process.return_value = saved_entity
        repository.save.return_value = saved_entity

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act, ejecuta el caso de uso
        result = use_case.execute(dto)

        # Assert, verifica que el resultado sea correcto
        assert result is not None
        assert isinstance(result, MessageResponseDTO)
        assert result.message_id == "msg-123"
        assert result.session_id == "session-abc"
        assert result.content == "Hello world"
        assert result.sender == "user"
        assert result.metadata is not None
        assert result.metadata["word_count"] == 2
        assert result.metadata["character_count"] == 11

    #Debe llamar al filtro de contenido para validar el contenido del mensaje
    def test_create_message_calls_content_filter(self):
        # Arrange, prepara los mocks y datos de prueba
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        content_filter.filter.return_value = "filtered content"

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="test content",
            timestamp=datetime.now(),
            sender="user"
        )

        # Mock para el entity devuelto
        entity = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="filtered content",
            timestamp=datetime.now(),
            sender=SenderType.USER
        )
        message_processor.process.return_value = entity
        repository.save.return_value = entity

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act, ejecuta el caso de uso
        use_case.execute(dto)

        # Assert, verifica que el filtro de contenido fue llamado
        content_filter.filter.assert_called_once_with("test content")

    #Debe llamar al procesador de mensajes para agregar metadatos
    def test_create_message_calls_message_processor(self):
        # Arrange, prepara los mocks y datos de prueba
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        content_filter.filter.return_value = "content"

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="test",
            timestamp=datetime.now(),
            sender="system"
        )

        entity = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="content",
            timestamp=datetime.now(),
            sender=SenderType.SYSTEM
        )
        message_processor.process.return_value = entity
        repository.save.return_value = entity

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act, ejecuta el caso de uso
        use_case.execute(dto)

        # Assert, verifica que el procesador de mensajes fue llamado
        message_processor.process.assert_called_once()

    #Debe guardar el mensaje procesado en el repositorio
    def test_create_message_persists_to_repository(self):
        # Arrange, prepara los mocks y datos de prueba
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        content_filter.filter.return_value = "content"

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="test",
            timestamp=datetime.now(),
            sender="user"
        )

        entity = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="content",
            timestamp=datetime.now(),
            sender=SenderType.USER
        )
        message_processor.process.return_value = entity
        repository.save.return_value = entity

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act, ejecuta el caso de uso
        use_case.execute(dto)

        # Assert, verifica que el repositorio guardó el mensaje
        repository.save.assert_called_once()

#Tests para la validación del contenido durante la creación de mensajes
class TestCreateMessageUseCaseContentFiltering:

    def test_create_message_with_inappropriate_content_raises_error(self):
        """Should raise ValueError when content contains inappropriate words."""
        # Arrange
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        content_filter.filter.side_effect = ValueError("Content contains inappropriate words")

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="buy this spam now",
            timestamp=datetime.now(),
            sender="user"
        )

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Content contains inappropriate words"):
            use_case.execute(dto)

    def test_create_message_filters_content_before_saving(self):
        """Should use filtered content when saving, not original content."""
        # Arrange
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        original_content = "  hello world  "
        filtered_content = "hello world"

        content_filter.filter.return_value = filtered_content

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content=original_content,
            timestamp=datetime.now(),
            sender="user"
        )

        entity = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content=filtered_content,
            timestamp=datetime.now(),
            sender=SenderType.USER
        )
        message_processor.process.return_value = entity
        repository.save.return_value = entity

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act
        use_case.execute(dto)

        # Assert - verify filtered content was used
        saved_entity = message_processor.process.call_args[0][0]
        assert saved_entity.content == filtered_content


class TestCreateMessageUseCaseSenderValidation:
    """Tests for sender validation."""

    def test_create_message_with_valid_user_sender(self):
        """Should accept 'user' as valid sender."""
        # Arrange
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        content_filter.filter.return_value = "content"

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="test",
            timestamp=datetime.now(),
            sender="user"
        )

        entity = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="content",
            timestamp=datetime.now(),
            sender=SenderType.USER
        )
        message_processor.process.return_value = entity
        repository.save.return_value = entity

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act & Assert - should not raise
        result = use_case.execute(dto)
        assert result is not None

    def test_create_message_with_valid_system_sender(self):
        """Should accept 'system' as valid sender."""
        # Arrange
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        content_filter.filter.return_value = "content"

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="test",
            timestamp=datetime.now(),
            sender="system"
        )

        entity = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="content",
            timestamp=datetime.now(),
            sender=SenderType.SYSTEM
        )
        message_processor.process.return_value = entity
        repository.save.return_value = entity

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act & Assert
        result = use_case.execute(dto)
        assert result.sender == "system"

    def test_create_message_with_invalid_sender_raises_error(self):
        """Should raise ValueError for invalid sender type."""
        # Arrange
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        content_filter.filter.return_value = "content"

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="test",
            timestamp=datetime.now(),
            sender="invalid_sender"
        )

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act & Assert
        with pytest.raises(ValueError):
            use_case.execute(dto)


class TestCreateMessageUseCaseEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_create_message_with_empty_message_id_raises_error(self):
        """Should raise ValueError when message_id is empty."""
        # Arrange
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        dto = CreateMessageDTO(
            message_id="",
            session_id="session-abc",
            content="test",
            timestamp=datetime.now(),
            sender="user"
        )

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act & Assert
        with pytest.raises(ValueError, match="message_id cannot be empty"):
            use_case.execute(dto)

    def test_create_message_with_empty_session_id_raises_error(self):
        """Should raise ValueError when session_id is empty."""
        # Arrange
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="",
            content="test",
            timestamp=datetime.now(),
            sender="user"
        )

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act & Assert
        with pytest.raises(ValueError, match="session_id cannot be empty"):
            use_case.execute(dto)

    def test_create_message_with_empty_content_raises_error(self):
        """Should raise ValueError when content is empty."""
        # Arrange
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="",
            timestamp=datetime.now(),
            sender="user"
        )

        content_filter.filter.return_value = ""

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act & Assert
        with pytest.raises(ValueError, match="content cannot be empty"):
            use_case.execute(dto)

    def test_create_message_with_whitespace_only_content_raises_error(self):
        """Should raise ValueError when content is only whitespace."""
        # Arrange
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        dto = CreateMessageDTO(
            message_id="msg-123",
            session_id="session-abc",
            content="   ",
            timestamp=datetime.now(),
            sender="user"
        )

        content_filter.filter.return_value = ""  # After sanitization

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )

        # Act & Assert
        with pytest.raises(ValueError, match="content cannot be empty"):
            use_case.execute(dto)
