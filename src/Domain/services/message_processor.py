"""
Domain Layer - Message Processor Service
Servicio de dominio para procesar mensajes y agregar metadatos.
"""
from datetime import datetime
from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.message_metadata import MessageMetadata


class MessageProcessor:
    """
    Servicio de dominio que procesa mensajes y agrega metadatos.
    """

    def process(self, message: MessageEntity) -> MessageEntity:
        """
        Procesa el mensaje y retorna una nueva instancia con metadatos.
        """

        word_count = len(message.content.split())
        character_count = len(message.content)

        metadata = MessageMetadata(
            word_count=word_count,
            character_count=character_count,
            processed_at=datetime.utcnow()
        )

        return message.with_metadata(metadata)
