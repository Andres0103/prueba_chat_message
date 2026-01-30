#Importante: Este archivo contiene la configuración de la aplicación cargada desde variables de entorno.
import os
from dataclasses import dataclass

#Configuración de la aplicación cargada desde variables de entorno
@dataclass
class Settings:
    
    # Application
    APP_NAME: str = "chat-message-api"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:////app/data/chat_messages.db"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    def __post_init__(self):
        # Cargar variables de entorno si están definidas
        self.APP_NAME = os.getenv("APP_NAME", self.APP_NAME)
        self.APP_VERSION = os.getenv("APP_VERSION", self.APP_VERSION)
        self.DEBUG = os.getenv("DEBUG", str(self.DEBUG)).lower() == "true"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", self.ENVIRONMENT)
        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)
        self.HOST = os.getenv("HOST", self.HOST)
        self.PORT = int(os.getenv("PORT", str(self.PORT)))


# Singleton de configuración para ser usado en toda la aplicación
settings = Settings()