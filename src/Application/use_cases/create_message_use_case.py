from src.Domain.entities.message_entity import MessageEntity
from src.Domain.value_objects.sender_type import SenderType
from src.Application.dtos.message_dto import CreateMessageDTO, MessageResponseDTO
from src.Application.interfaces.message_repository_interface import MessageRepositoryInterface
from src.Domain.services.content_filter import ContentFilterService as ContentFilter
from src.Domain.services.message_processor import MessageProcessor

class CreateMessageUseCase:
    """
    Caso de uso para crear y procesar un mensaje.
    Orquesta las reglas del dominio y la persistencia.
    """

    def __init__(
        self,
        repository: MessageRepositoryInterface,
        content_filter: ContentFilter,
        message_processor: MessageProcessor
    ):
        self.repository = repository
        self.content_filter = content_filter
        self.message_processor = message_processor

    def execute(self, dto: CreateMessageDTO) -> MessageResponseDTO:
        """
        Ejecuta el flujo de creación del mensaje.
        """

        sender = SenderType(dto.sender)

        filtered_content = self.content_filter.filter(dto.content)

        message = MessageEntity(
            message_id=dto.message_id,
            session_id=dto.session_id,
            content=filtered_content,
            timestamp=dto.timestamp,
            sender=sender
        )

        processed_message = self.message_processor.process(message)

        saved_message = self.repository.save(processed_message)

        return MessageResponseDTO(
            message_id=saved_message.message_id,
            session_id=saved_message.session_id,
            content=saved_message.content,
            timestamp=saved_message.timestamp,
            sender=saved_message.sender.value,
            metadata=saved_message.metadata.to_dict() if saved_message.metadata else None
        )
