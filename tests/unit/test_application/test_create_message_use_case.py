#Test para la creación de mensajes en la aplicación
import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock, AsyncMock

from src.Application.use_cases.create_message_use_case import CreateMessageUseCase
from src.Application.dtos.message_dto import CreateMessageDTO, MessageResponseDTO
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Domain.value_objects.message_metadata import MessageMetadata

#Test para la creación de mensajes en la aplicación
@pytest.mark.asyncio
class TestCreateMessageUseCaseSuccess:

    #Debe crear un mensaje con datos válidos y devolver MessageResponseDTO
    async def test_create_message_with_valid_data_returns_response_dto(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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
        # Ejecuta el caso de uso
        result = await use_case.execute(dto)

        # Verifica que el resultado sea correcto
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
    async def test_create_message_calls_content_filter(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
        content_filter = Mock()
        message_processor = Mock()

        content_filter.filter.return_value = "contenido filtrado"

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
            content="contenido filtrado",
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

        # Ejecuta el caso de uso
        await use_case.execute(dto)

        # Verifica que el filtro de contenido fue llamado
        content_filter.filter.assert_called_once_with("test content")

    #Debe llamar al procesador de mensajes para agregar metadatos
    async def test_create_message_calls_message_processor(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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

        # Ejecuta el caso de uso
        await use_case.execute(dto)

        # Verifica que el procesador de mensajes fue llamado
        message_processor.process.assert_called_once()

    #Debe guardar el mensaje procesado en el repositorio
    async def test_create_message_persists_to_repository(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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
        # ejecuta el caso de uso
        await use_case.execute(dto)

        # Verifica que el repositorio guardó el mensaje
        repository.save.assert_awaited_once()

#Tests para la validación del contenido durante la creación de mensajes
@pytest.mark.asyncio
class TestCreateMessageUseCaseContentFiltering:

    #Debe lanzar ValueError si el contenido tiene palabras inapropiadas
    async def test_create_message_with_inappropriate_content_raises_error(self):
        # Prepara los mocks y datos de prueba
        repository = Mock()
        content_filter = Mock()
        message_processor = Mock()

        content_filter.filter.side_effect = ValueError("El mensaje contiene palabras inapropiadas")

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

        with pytest.raises(ValueError, match="El mensaje contiene palabras inapropiadas"):
            await use_case.execute(dto)

    #Debe usar el contenido filtrado al guardar, no el original
    async def test_create_message_filters_content_before_saving(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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
        await use_case.execute(dto)

        # Verifica que el contenido guardado es el filtrado
        saved_entity = message_processor.process.call_args[0][0]
        assert saved_entity.content == filtered_content


@pytest.mark.asyncio
class TestCreateMessageUseCaseSenderValidation:

    #Debe aceptar 'user' como remitente válido
    async def test_create_message_with_valid_user_sender(self):
        # prepara los mocks y datos de prueba
        repository = AsyncMock()
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
        result = await use_case.execute(dto)
        assert result is not None

    #Debe aceptar 'system' como remitente válido
    async def test_create_message_with_valid_system_sender(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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
        result = await use_case.execute(dto)
        assert result.sender == "system"

    #Debe lanzar ValueError para tipos de remitente no válidos
    async def test_create_message_with_invalid_sender_raises_error(self):
        # Prepara los mocks y datos de prueba
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
        with pytest.raises(ValueError):
            await use_case.execute(dto)

#Tests para casos límite y condiciones de borde
@pytest.mark.asyncio
class TestCreateMessageUseCaseEdgeCases:

    #Debe lanzar ValueError si message_id está vacío
    async def test_create_message_with_empty_message_id_raises_error(self):
        # Prepara los mocks y datos de prueba
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
        with pytest.raises(ValueError, match="message_id no puede estar vacío"):
            await use_case.execute(dto)

    #Debe lanzar ValueError si session_id está vacío
    async def test_create_message_with_empty_session_id_raises_error(self):
        # Prepara los mocks y datos de prueba
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
        with pytest.raises(ValueError, match="session_id no puede estar vacío"):
            await use_case.execute(dto)

    #Debe lanzar ValueError si el contenido está vacío después del filtrado
    async def test_create_message_with_empty_content_raises_error(self):
        # Prepara los mocks y datos de prueba
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
        with pytest.raises(ValueError, match="content no puede estar vacío"):
            await use_case.execute(dto)

    #Debe lanzar ValueError si el contenido es solo espacios en blanco después del filtrado
    async def test_create_message_with_whitespace_only_content_raises_error(self):
        # Prepara los mocks y datos de prueba
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

        content_filter.filter.return_value = ""  # después del filtrado queda vacío

        use_case = CreateMessageUseCase(
            repository=repository,
            content_filter=content_filter,
            message_processor=message_processor
        )
        # Act & Assert
        with pytest.raises(ValueError, match="content no puede estar vacío"):
            await use_case.execute(dto)
