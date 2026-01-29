from enum import Enum


class SenderType(str, Enum):
    """
    Value Object que representa el tipo de remitente del mensaje.
    """

    USER = "user"
    SYSTEM = "system"
