"""
Main application entry point.
"""
from fastapi import FastAPI

from src.Infrastructure.config.settings import settings
from src.Infrastructure.database.connection import create_tables

from src.API.v1.controllers.message_controller import router as message_router
from src.API.exceptions.handlers import register_exception_handlers

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="API RESTful para procesamiento de mensajes de chat"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    create_tables()


# Registrar routers
app.include_router(message_router)

# Registrar handlers de errores
register_exception_handlers(app)


@app.get("/")
async def root():
    return {
        "message": "Chat Message API",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }
