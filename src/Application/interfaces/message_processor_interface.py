#Importante: Este archivo define la interfaz para servicios de procesamiento de mensajes en la aplicación.
#Importar las librerías necesarias
from abc import ABC, abstractmethod
from src.Domain.entities.message_entity import MessageEntity

#MensajeProcessorInterface define el contrato para servicios que procesan mensajes - Contrato quiere decir que las implementaciones concretas vivirán en infrastructure
class MessageProcessorInterface(ABC):
    """
    Interfaz para servicios que procesan mensajes.
    """

    @abstractmethod
    def process(self, message: MessageEntity) -> MessageEntity:
        pass
