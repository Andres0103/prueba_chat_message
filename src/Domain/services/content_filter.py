"""
Domain Layer - Content Filter Service
Servicio de dominio que contiene lógica de negocio para filtrar contenido inapropiado.
"""
from typing import List, Tuple


class ContentFilterService:
    """
    Servicio de dominio para filtrar contenido inapropiado.
    Contiene lógica de negocio pura sin dependencias externas.
    """
    
    # Lista simple de palabras prohibidas (se puede extender)
    INAPPROPRIATE_WORDS: List[str] = [
        "spam",
        "malware",
        "phishing",
        "scam",
        # Agregar más palabras según necesidad
    ]
    
    @classmethod
    def contains_inappropriate_content(cls, content: str) -> bool:
        """
        Verifica si el contenido contiene palabras inapropiadas.
        
        Args:
            content: El contenido del mensaje a verificar
            
        Returns:
            True si contiene contenido inapropiado, False en caso contrario
        """
        content_lower = content.lower()
        return any(word in content_lower for word in cls.INAPPROPRIATE_WORDS)
    
    @classmethod
    def filter_content(cls, content: str) -> Tuple[bool, str]:
        """
        Filtra el contenido y retorna si es válido y un mensaje de error si aplica.
        
        Args:
            content: El contenido del mensaje a filtrar
            
        Returns:
            Tupla con (is_valid, error_message)
        """
        if cls.contains_inappropriate_content(content):
            return False, "Content contains inappropriate words"
        
        return True, ""
    
    @classmethod
    def sanitize_content(cls, content: str) -> str:
        """
        Sanitiza el contenido removiendo espacios extras.
        
        Args:
            content: El contenido a sanitizar
            
        Returns:
            Contenido sanitizado
        """
        return content.strip()