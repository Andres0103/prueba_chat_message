#Importante: Este archivo define la interfaz para servicios de filtrado de contenido en la aplicación.
#Importar las librerías necesarias
from abc import ABC, abstractmethod

#Construida la interfaz de filtrado de contenido - Interface para servicios de filtrado de contenido
class ContentFilterInterface(ABC):
    @abstractmethod
    def filter(self, content: str) -> str:
        """
        Valida y sanitiza el contenido.
        Lanza excepción si el contenido es inválido.
        """
        pass
