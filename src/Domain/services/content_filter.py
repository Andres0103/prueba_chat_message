#Importante: Este archivo define el servicio de dominio para filtrar contenido inapropiado.
from src.Application.interfaces.content_filter_interface import ContentFilterInterface

#Servicio de dominio para filtrar contenido inapropiado, heredando de la interfaz definida para el filtro de contenido
class ContentFilterService(ContentFilterInterface):
    INAPPROPRIATE_WORDS = {"spam", "malware", "hack", "scam"} 

    def filter(self, content: str) -> str:
        """
        Valida y sanitiza el contenido.
        Lanza excepción si el contenido es inválido.
        """
        sanitized = self.sanitize_content(content)
        
        if self.contains_inappropriate_content(sanitized):
            raise ValueError("El mensaje contiene palabras inapropiadas.")
        
        return sanitized

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
            return False, "El mensaje contiene palabras inapropiadas"

        return True, ""
