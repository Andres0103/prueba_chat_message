#Importante: Este archivo define el servicio de dominio para filtrar contenido inapropiado.
from typing import List, Tuple
from src.Application.interfaces.content_filter_interface import ContentFilterInterface

#Servicio de dominio para filtrar contenido inapropiado, heredando de la interfaz definida para el filtro de contenido
class ContentFilterService(ContentFilterInterface):
    
    # Lista simple de palabras prohibidas (se puede extender)
    INAPPROPRIATE_WORDS: List[str] = [
        "spam",
        "malware",
        "phishing",
        "scam",
    ]
    
    @classmethod
    def filter(cls, content: str) -> str:
        #lanza una excepción si el contenido es inapropiado y valida el contenido
        content = content.strip()
        content_lower = content.lower()

        for word in cls.INAPPROPRIATE_WORDS:
            if word in content_lower:
                raise ValueError(f"El contenido contiene palabra inapropiada: {word}")

        return content
    
    @classmethod
    def filter_content(cls, content: str) -> Tuple[bool, str]:
        #Filtra el contenido y retorna si es apropiado junto con un mensaje
        if cls.contains_inappropriate_content(content):
            return False, "Contenido inapropiado detectado."
        
        return True, ""
    
    @classmethod
    def sanitize_content(cls, content: str) -> str:
        #Elimina espacios en blanco innecesarios del contenido, lo sanitiza
        return content.strip()