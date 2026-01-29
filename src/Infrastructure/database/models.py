"""
Infrastructure Layer - SQLAlchemy Models
Este archivo contiene los modelos de base de datos usando SQLAlchemy ORM.
Pertenece a Infrastructure porque es una implementación técnica específica.
"""
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MessageModel(Base):
    """
    Modelo de base de datos para mensajes.
    Este es el modelo ORM que representa la tabla en SQLite.
    """
    
    __tablename__ = "messages"
    
    # Campos básicos del mensaje (según PDF)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    message_id = Column(String, unique=True, nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    sender = Column(String, nullable=False)  # "user" o "system"
    
    # Metadatos procesados
    word_count = Column(Integer, nullable=True)
    character_count = Column(Integer, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Message(message_id={self.message_id}, session_id={self.session_id})>"