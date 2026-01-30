#Importante: Este archivo define los tipos de remitentes de mensajes en la aplicación.
from enum import Enum

#Value Object que representa el tipo de remitente del mensaje
class SenderType(str, Enum):
    USER = "user"
    SYSTEM = "system"
