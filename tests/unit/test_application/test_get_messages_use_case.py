"""
Unit tests for GetMessagesUseCase.
Tests cover: successful retrieval, pagination, filtering, error handling, and edge cases.
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock

from src.Application.use_cases.get_messages_use_case import GetMessagesUseCase
from src.Application.dtos.pagination_dto import PaginationDTO, GetMessagesFilterDTO
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Domain.value_objects.message_metadata import MessageMetadata

#Test para obtener mensajes exitosamente
@pytest.mark.asyncio
class TestGetMessagesUseCaseSuccess:

    #Debe retornar una respuesta paginada con los mensajes
    async def test_get_messages_returns_paginated_response(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()

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

        result = await use_case.execute(filters)

        # Verifica los resultados
        assert result is not None
        assert isinstance(result, PaginationDTO)
        assert isinstance(result.items, list)
        assert len(result.items) == 2
        assert result.limit == 10
        assert result.offset == 0
        assert result.total == 2

    #Debe retornar una lista vacía cuando no hay mensajes para la sesión
    async def test_get_messages_with_no_messages_returns_empty_list(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
        repository.get_by_session.return_value = []
        repository.count_by_session.return_value = 0

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-empty",
            limit=10,
            offset=0
        )

        result = await use_case.execute(filters)

        assert result.items == []
        assert result.total == 0
        assert result.limit == 10
        assert result.offset == 0

    #Debe llamar al repositorio con los parámetros correctos
    async def test_get_messages_calls_repository_with_correct_params(self):
        # pREpara los mocks y datos de prueba
        repository = AsyncMock()
        repository.get_by_session.return_value = []
        repository.count_by_session.return_value = 0

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-123",
            limit=20,
            offset=10,
            sender="user"
        )

        await use_case.execute(filters)

        repository.get_by_session.assert_awaited_once_with(
            session_id="session-123",
            limit=20,
            offset=10,
            sender="user",
        )

#Tests para paginación
@pytest.mark.asyncio
class TestGetMessagesUseCasePagination:

    #Debe respetar el parámetro de límite para la paginación
    async def test_get_messages_respects_limit_parameter(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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

        repository.get_by_session.return_value = messages[:3]  # Simula retornar solo 3 mensajes
        repository.count_by_session.return_value = 5

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=3,
            offset=0
        )

        result = await use_case.execute(filters)

        assert len(result.items) == 3
        assert result.limit == 3
        assert result.total == 5

    #Debe respetar el parámetro de offset para la paginación
    async def test_get_messages_respects_offset_parameter(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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
        # Simula retornar mensajes a partir del offset 3    
        repository.get_by_session.return_value = messages
        repository.count_by_session.return_value = 5

        #Esto hace que se use offset 3 y limit 10
        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=10,
            offset=3
        )

        result = await use_case.execute(filters)

        assert result.offset == 3
        assert result.total == 5

    #Debe aceptar el límite máximo de 100 sin error
    async def test_get_messages_with_max_limit_100(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
        repository.get_by_session.return_value = []
        repository.count_by_session.return_value = 0

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=100,  # Limite máximo permitido
            offset=0
        )

        result = await use_case.execute(filters)

        call_args = repository.get_by_session.call_args
        assert call_args[1]["limit"] == 100

#Tests para filtrado de mensajes
@pytest.mark.asyncio
class TestGetMessagesUseCaseFiltering:

    #Debe filtrar mensajes por tipo de remitente 'user'
    async def test_get_messages_filters_by_user_sender(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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

        result = await use_case.execute(filters)

        repository.get_by_session.assert_awaited_once()
        call_args = repository.get_by_session.call_args
        assert call_args[1]["sender"] == "user"
        assert all(msg.sender == SenderType.USER for msg in result.items)

    #Debe filtrar mensajes por tipo de remitente 'system'
    async def test_get_messages_filters_by_system_sender(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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

        result = await use_case.execute(filters)

        call_args = repository.get_by_session.call_args
        assert call_args[1]["sender"] == "system"
        assert all(msg.sender == SenderType.SYSTEM for msg in result.items)

    #Debe retornar mensajes de todos los remitentes cuando no se especifica filtro
    async def test_get_messages_returns_all_senders_when_no_filter(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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

        result = await use_case.execute(filters)

        call_args = repository.get_by_session.call_args
        assert call_args[1]["sender"] is None
        assert len(result.items) == 2

#Tests para validación de entrada
@pytest.mark.asyncio
class TestGetMessagesUseCaseValidation:

    #Debe lanzar ValueError cuando session_id está vacío
    async def test_get_messages_with_empty_session_id_raises_error(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
        use_case = GetMessagesUseCase(repository)

        filters = GetMessagesFilterDTO(
            session_id="",
            limit=10,
            offset=0
        )

        with pytest.raises(ValueError, match="session_id no puede estar vacío"):
            await use_case.execute(filters)

#Tests para casos límite y condiciones de borde
@pytest.mark.asyncio
class TestGetMessagesUseCaseEdgeCases:

    #Debe aceptar el límite mínimo de 1 sin error
    async def test_get_messages_with_limit_1_is_valid(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
        repository.get_by_session.return_value = []
        repository.count_by_session.return_value = 0

        use_case = GetMessagesUseCase(repository)
        filters = GetMessagesFilterDTO(
            session_id="session-abc",
            limit=1,
            offset=0
        )

        result = await use_case.execute(filters)

        call_args = repository.get_by_session.call_args
        assert call_args[1]["limit"] == 1

    #Debe retornar mensajes ordenados por timestamp ascendente
    async def test_get_messages_ordered_by_timestamp_ascending(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()

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

        result = await use_case.execute(filters)

        assert len(result.items) == 2
        assert result.items[0].message_id == "msg-1"
        assert result.items[1].message_id == "msg-2"

    #Debe retornar solo mensajes de la sesión especificada
    async def test_get_messages_returns_only_specified_session(self):
        # Prepara los mocks y datos de prueba
        repository = AsyncMock()
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

        result = await use_case.execute(filters)

        repository.get_by_session.assert_awaited_once()
        call_args = repository.get_by_session.call_args
        assert call_args[1]["session_id"] == "session-abc"
        assert all(msg.session_id == "session-abc" for msg in result.items)


