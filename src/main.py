#Importante: Este archivo es el punto de entrada principal de la aplicación FastAPI.
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
    create_tables()

    base_url = f"http://{settings.HOST}:{settings.PORT}"

    print("=" * 60)
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} started")
    print(f"API Base URL:      {base_url}")
    print(f"Swagger Docs:     {base_url}/docs")
    print(f"ReDoc Docs:       {base_url}/redoc")
    print(f"Database URL:     {settings.DATABASE_URL}")
    print("=" * 60)



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
