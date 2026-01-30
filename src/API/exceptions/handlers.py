#Importar los módulos necesarios

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.API.v1.schemas.error_schema import ErrorResponse, ErrorDetail

#Función para registrar los handlers de excepciones
def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                error=ErrorDetail(
                    code="INVALID_FORMAT",
                    message=str(exc),
                    details=str(exc),
                )
            ).dict()
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error=ErrorDetail(
                    code="INTERNAL_SERVER_ERROR",
                    message="An unexpected error occurred",
                    details=str(exc),
                )
            ).dict()
        )
