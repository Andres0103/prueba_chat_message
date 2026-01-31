#Importante: Este archivo contiene la implementación concreta del repositorio de mensajes usando SQLAlchemy.
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from src.Application.interfaces.message_repository_interface import MessageRepositoryInterface
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Domain.value_objects.message_metadata import MessageMetadata

from src.Infrastructure.database.models import MessageModel


class MessageRepositoryImpl(MessageRepositoryInterface):

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save(self, message: MessageEntity) -> MessageEntity:
        model = MessageModel(
            message_id=message.message_id,
            session_id=message.session_id,
            content=message.content,
            timestamp=message.timestamp,
            sender=message.sender.value,
            word_count=message.metadata.word_count if message.metadata else None,
            character_count=message.metadata.character_count if message.metadata else None,
            processed_at=message.metadata.processed_at if message.metadata else None,
        )

        self.db_session.add(model)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(model)
        except IntegrityError as e:
            # Map DB integrity issues (e.g. unique constraint on message_id)
            await self.db_session.rollback()
            # Raise a ValueError so upper layers (use-case/controller) can return 400
            raise ValueError(f"El mensaje con id {message.message_id} ya existe o hay un error de integridad en la base de datos") from e

        return self._to_entity(model)

    async def get_by_session(
        self,
        session_id: str,
        limit: int,
        offset: int,
        sender: Optional[str] = None,
    ) -> List[MessageEntity]:
        stmt = select(MessageModel).where(MessageModel.session_id == session_id)

        if sender:
            stmt = stmt.where(MessageModel.sender == sender)

        stmt = stmt.order_by(MessageModel.timestamp.asc()).offset(offset).limit(limit)

        result = await self.db_session.execute(stmt)
        rows = result.scalars().all()

        return [self._to_entity(m) for m in rows]

    async def count_by_session(self, session_id: str, sender: Optional[str] = None) -> int:
        stmt = select(func.count()).select_from(MessageModel).where(MessageModel.session_id == session_id)
        if sender:
            stmt = stmt.where(MessageModel.sender == sender)

        result = await self.db_session.execute(stmt)
        count = result.scalar_one()
        return int(count)

    def _to_entity(self, model: MessageModel) -> MessageEntity:
        metadata = None
        if model.word_count is not None:
            metadata = MessageMetadata(
                word_count=model.word_count,
                character_count=model.character_count,
                processed_at=model.processed_at,
            )

        return MessageEntity(
            message_id=model.message_id,
            session_id=model.session_id,
            content=model.content,
            timestamp=model.timestamp,
            sender=SenderType(model.sender),
            metadata=metadata,
        )
