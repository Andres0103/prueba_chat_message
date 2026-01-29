from abc import ABC, abstractmethod
from typing import List, Optional
from src.Domain.entities.message_entity import MessageEntity

class MessageRepositoryInterface(ABC):
    """
    Interface que define el contrato para la persistencia de mensajes.
    Implementaciones concretas viven en infrastructure.
    """

    @abstractmethod
    def save(self, message: MessageEntity) -> MessageEntity:
        """
        Guarda un mensaje y retorna el mensaje persistido.
        """
        pass

    @abstractmethod
    def get_by_session(
        self,
        session_id: str,
        limit: int,
        offset: int,
        sender: Optional[str] = None
    ) -> List[MessageEntity]:
        """
        Obtiene mensajes por sesión con paginación y filtro opcional por remitente.
        """
        pass
