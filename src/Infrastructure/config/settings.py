"""
Infrastructure Layer - Configuration Settings
Este archivo pertenece a Infrastructure porque maneja configuraciones técnicas.
"""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "chat-message-api"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "sqlite:///./chat_messages.db"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    def __post_init__(self):
        """Load from environment variables if available."""
        self.APP_NAME = os.getenv("APP_NAME", self.APP_NAME)
        self.APP_VERSION = os.getenv("APP_VERSION", self.APP_VERSION)
        self.DEBUG = os.getenv("DEBUG", str(self.DEBUG)).lower() == "true"
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", self.ENVIRONMENT)
        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)
        self.HOST = os.getenv("HOST", self.HOST)
        self.PORT = int(os.getenv("PORT", str(self.PORT)))


# Singleton instance
settings = Settings()