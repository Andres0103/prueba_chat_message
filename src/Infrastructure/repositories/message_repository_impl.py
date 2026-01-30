#Importante: Este archivo contiene la implementación concreta del repositorio de mensajes usando SQLAlchemy.
from typing import List, Optional

from sqlalchemy.orm import Session

from src.Application.interfaces.message_repository_interface import MessageRepositoryInterface
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Domain.value_objects.message_metadata import MessageMetadata

from src.Infrastructure.database.models import MessageModel

#Clase que implementa el repositorio de mensajes usando SQLAlchemy
class MessageRepositoryImpl(MessageRepositoryInterface):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    #Guarda un mensaje en la base de datos y retorna la entidad persistida
    def save(self, message: MessageEntity) -> MessageEntity:

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
        self.db_session.commit()
        self.db_session.refresh(model)

        return self._to_entity(model)

    #Obtiene mensajes por sesión con paginación y filtro opcional por sender
    def get_by_session(
        self,
        session_id: str,
        limit: int,
        offset: int,
        sender: Optional[str] = None
    ) -> List[MessageEntity]:
        
        query = self.db_session.query(MessageModel).filter(
            MessageModel.session_id == session_id
        )

        if sender:
            query = query.filter(MessageModel.sender == sender)

        results = (
            query
            .order_by(MessageModel.timestamp.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return [self._to_entity(model) for model in results]

    #Cuenta el total de mensajes en una sesión, opcionalmente filtrados por sender
    def count_by_session(
        self,
        session_id: str,
        sender: Optional[str] = None
    ) -> int:

        query = self.db_session.query(MessageModel).filter(
            MessageModel.session_id == session_id
        )

        if sender:
            query = query.filter(MessageModel.sender == sender)

        return query.count()

    #Convierte un modelo ORM en una entidad de dominio
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
