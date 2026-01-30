#Importante: Este archivo define el servicio de dominio para filtrar contenido inapropiado.
from typing import List, Tuple
from src.Application.interfaces.content_filter_interface import ContentFilterInterface

#Servicio de dominio para filtrar contenido inapropiado, heredando de la interfaz definida para el filtro de contenido
class ContentFilterService:
    INAPPROPRIATE_WORDS = {"spam", "malware", "hack"}

    @classmethod
    def contains_inappropriate_content(cls, content: str) -> bool:
        if not content:
            return False

        content_lower = content.lower()
        return any(word in content_lower for word in cls.INAPPROPRIATE_WORDS)

    @classmethod
    def sanitize_content(cls, content: str) -> str:
        return content.strip()

    @classmethod
    def filter_content(cls, content: str):
        sanitized = cls.sanitize_content(content)

        if cls.contains_inappropriate_content(sanitized):
            return False, "Content contains inappropriate words"

        return True, ""
