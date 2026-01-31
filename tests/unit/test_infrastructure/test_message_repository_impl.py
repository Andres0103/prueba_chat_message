#Test para MessageRepositoryImpl
import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.Infrastructure.repositories.message_repository_impl import MessageRepositoryImpl
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Domain.value_objects.message_metadata import MessageMetadata
from src.Infrastructure.database.models import MessageModel
#test para MessageRepositoryImpl
class TestMessageRepositoryImpl:

    #Este test se hizo de esta manera ya que el repositorio usa AsyncSession de SQLAlchemy y necesitamos mockear su comportamiento para las pruebas unitarias.

    #Mock de AsyncSession de SQLAlchemy
    @pytest.fixture
    def mock_db_session(self):
        return AsyncMock(spec=AsyncSession)

    #Instancia del repositorio con mock de BD
    @pytest.fixture
    def repository(self, mock_db_session):
        return MessageRepositoryImpl(mock_db_session)

    #Debe guardar un mensaje exitosamente en la BD
    @pytest.mark.asyncio
    async def test_save_message_successfully(self, repository, mock_db_session):
        metadata = MessageMetadata(
            word_count=2,
            character_count=12,
            processed_at=datetime.utcnow()
        )
        
        message = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="Test message",
            timestamp=datetime.utcnow(),
            sender=SenderType.USER,
            metadata=metadata
        )

        mock_db_session.refresh = AsyncMock()
        mock_db_session.add = MagicMock()
        mock_db_session.commit = AsyncMock()

        result = await repository.save(message)

        assert result is not None
        assert result.message_id == "msg-123"
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    #Debe obtener mensajes por session_id con paginación
    @pytest.mark.asyncio
    async def test_get_message_by_session(self, repository, mock_db_session):
        session_id = "session-abc"
        limit = 10
        offset = 0
        
        #Se crean modelos mock para simular los resultados de la BD
        model1 = MagicMock(spec=MessageModel)
        model1.message_id = "msg-1"
        model1.session_id = session_id
        model1.content = "Message 1"
        model1.timestamp = datetime.utcnow()
        model1.sender = "user"
        model1.word_count = 2
        model1.character_count = 10
        model1.processed_at = datetime.utcnow()
        
        model2 = MagicMock(spec=MessageModel)
        model2.message_id = "msg-2"
        model2.session_id = session_id
        model2.content = "Message 2"
        model2.timestamp = datetime.utcnow()
        model2.sender = "system"
        model2.word_count = 2
        model2.character_count = 10
        model2.processed_at = datetime.utcnow()

        # Mock: .all() retorna los modelos
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [model1, model2]
        
        # Mock: result.scalars() retorna el objeto con .all()
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        
        # execute() es AsyncMock
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session(
            session_id=session_id,
            limit=limit,
            offset=offset
        )

        assert result is not None
        assert len(result) == 2
        assert result[0].message_id == "msg-1"
        assert result[1].message_id == "msg-2"

    #Debe contar el total de mensajes de una sesión
    @pytest.mark.asyncio
    async def test_count_by_session(self, repository, mock_db_session):
        session_id = "session-abc"
        total_count = 25

        # Mock: scalar_one() retorna el conteo directamente
        mock_result = MagicMock()
        mock_result.scalar_one.return_value = total_count
        
        # execute() es AsyncMock
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        result = await repository.count_by_session(session_id)

        assert result == total_count
        mock_db_session.execute.assert_called_once()

    #Debe manejar IntegrityError y convertirlo en ValueError
    @pytest.mark.asyncio
    async def test_save_message_raises_integrity_error(self, repository, mock_db_session):
        from sqlalchemy.exc import IntegrityError
        
        metadata = MessageMetadata(
            word_count=2,
            character_count=12,
            processed_at=datetime.utcnow()
        )
        
        message = MessageEntity(
            message_id="msg-123",
            session_id="session-abc",
            content="Test",
            timestamp=datetime.utcnow(),
            sender=SenderType.USER,
            metadata=metadata
        )

        mock_db_session.add = MagicMock()
        mock_db_session.commit = AsyncMock(side_effect=IntegrityError("Duplicate", None, None))
        mock_db_session.rollback = AsyncMock()

        with pytest.raises(ValueError, match="ya existe"):
            await repository.save(message)
        
        mock_db_session.rollback.assert_called_once()

    #Debe retornar lista vacía cuando no hay mensajes
    @pytest.mark.asyncio
    async def test_get_by_session_empty_result(self, repository, mock_db_session):
        session_id = "session-nonexistent"

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session(
            session_id=session_id,
            limit=10,
            offset=0
        )

        assert result == []
        assert len(result) == 0

    #Debe filtrar mensajes por sender
    @pytest.mark.asyncio
    async def test_get_by_session_with_sender_filter(self, repository, mock_db_session):
        session_id = "session-abc"
        sender = "user"

        #Se crea un modelo mock para simular el resultado de la BD        
        model = MagicMock(spec=MessageModel)
        model.message_id = "msg-1"
        model.session_id = session_id
        model.content = "user message"
        model.timestamp = datetime.utcnow()
        model.sender = "user"
        model.word_count = 2
        model.character_count = 11
        model.processed_at = datetime.utcnow()

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = [model]
        
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        result = await repository.get_by_session(
            session_id=session_id,
            limit=10,
            offset=0,
            sender=sender
        )

        assert len(result) == 1
        assert result[0].sender == SenderType.USER