"""
Infrastructure Layer - Message Processor Implementation

Esta es la implementación CONCRETA del procesador de mensajes.
Implementa la interfaz IMessageProcessor definida en Application.

IMPORTANTE:
- Vive en Infrastructure porque es una implementación técnica
- Implementa la interfaz de Application
- Usa DTOs para comunicarse con otras capas
- Puede usar servicios de Domain directamente
"""
from datetime import datetime
from ...dtos.message_dto import MessageDTO, MessageMetadataDTO
from ...Application.interfaces.message_processor_interface import IMessageProcessor
from ...Domain.services.content_filter import ContentFilterService


class MessageProcessorImpl(IMessageProcessor):
    """
    Implementación concreta del procesador de mensajes.
    
    Responsabilidades:
    - Agregar metadatos a los mensajes (word_count, character_count)
    - Validar y sanitizar contenido (usa ContentFilterService)
    - Marcar timestamp de procesamiento
    """
    
    def process(self, message: MessageDTO) -> MessageDTO:
        """
        Procesa un mensaje y le agrega metadatos.
        
        Args:
            message: DTO del mensaje a procesar
            
        Returns:
            DTO del mensaje con metadatos agregados
            
        Raises:
            ValueError: Si el contenido es inválido
        """
        # Validar y sanitizar contenido
        sanitized_content = self.validate_and_sanitize(message.content)
        
        # Calcular metadatos
        word_count = len(sanitized_content.split())
        character_count = len(sanitized_content)
        
        # Crear DTO de metadatos
        metadata = MessageMetadataDTO(
            word_count=word_count,
            character_count=character_count,
            processed_at=datetime.utcnow()
        )
        
        # Retornar mensaje con metadatos
        return MessageDTO(
            message_id=message.message_id,
            session_id=message.session_id,
            content=sanitized_content,
            timestamp=message.timestamp,
            sender=message.sender,
            metadata=metadata
        )
    
    def validate_and_sanitize(self, content: str) -> str:
        """
        Valida y sanitiza el contenido usando el servicio de dominio.
        
        Args:
            content: Contenido a validar
            
        Returns:
            Contenido sanitizado
            
        Raises:
            ValueError: Si el contenido contiene palabras prohibidas
        """
        # Usar el servicio de dominio directamente
        is_valid, error_message = ContentFilterService.filter_content(content)
        
        if not is_valid:
            raise ValueError(error_message)
        
        # Retornar contenido sanitizado
        return ContentFilterService.sanitize_content(content)