#Importante: Este archivo define la interfaz para el repositorio de mensajes.
#Importar las librerías necesarias
from abc import ABC, abstractmethod
from typing import List, Optional
from src.Domain.entities.message_entity import MessageEntity

#Clase que define la interfaz del repositorio de mensajes - Define el contrato para la persistencia de mensajes
class MessageRepositoryInterface(ABC):

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

    @abstractmethod
    def count_by_session(
        self,
        session_id: str,
        sender: Optional[str] = None
    ) -> int:
        """
        Cuenta el total de mensajes en una sesión, opcionalmente filtrados por remitente.
        """
        pass
