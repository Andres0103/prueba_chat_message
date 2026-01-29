"""
Main application entry point.
"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.Infrastructure.config.settings import settings
from src.Infrastructure.database.connection import create_tables, get_db
from src.Infrastructure.database.models import MessageModel

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="API RESTful para procesamiento de mensajes de chat"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        create_tables()
        print("=" * 60)
        print(f"✅ Database initialized successfully")
        print(f"✅ Database URL: {settings.DATABASE_URL}")
        print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} started")
        print(f"✅ Server running on http://{settings.HOST}:{settings.PORT}")
        print(f"✅ Docs available at http://{settings.HOST}:{settings.PORT}/docs")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Chat Message API",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@app.get("/db-test")
async def test_database_connection(db: Session = Depends(get_db)):
    """
    Endpoint para probar la conexión a la base de datos.
    Intenta hacer una query simple.
    """
    try:
        # Intentar hacer una query simple
        result = db.query(MessageModel).count()
        return {
            "status": "success",
            "message": "Database connection successful",
            "messages_count": result,
            "database_url": settings.DATABASE_URL.split("///")[-1]  # Ocultar path completo
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )