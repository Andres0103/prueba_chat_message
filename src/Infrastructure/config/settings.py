# Importante: Este archivo contiene la configuración de la aplicación cargada desde variables de entorno.
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    # Application
    APP_NAME: str = "chat-message-api"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str | None = None

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    def __post_init__(self):
        self.APP_NAME = os.getenv("APP_NAME", self.APP_NAME)
        self.APP_VERSION = os.getenv("APP_VERSION", self.APP_VERSION)
        self.DEBUG = os.getenv("DEBUG", str(self.DEBUG)).lower() == "true"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", self.ENVIRONMENT)
        self.HOST = os.getenv("HOST", self.HOST)
        self.PORT = int(os.getenv("PORT", str(self.PORT)))

        # DATABASE_URL según entorno
        if os.getenv("DATABASE_URL"):
            self.DATABASE_URL = os.getenv("DATABASE_URL")
        else:
            if self.ENVIRONMENT == "docker":
                self.DATABASE_URL = "sqlite:////app/data/chat_messages.db"
            else:
                # local / windows
                Path("data").mkdir(exist_ok=True)
                self.DATABASE_URL = "sqlite:///./data/chat_messages.db"


# Singleton
settings = Settings()
