# src/infrastructure/api/error_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Dict, Any

class TaskNotFoundError(Exception):
    """Raised when a task cannot be found."""
    pass

class ValidationError(Exception):
    """Raised when validation fails."""
    pass

async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    """
    Handler for TaskNotFoundError.
    Returns 404 status code with error details.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Task not found",
            "type": "task_not_found",
            "status": status.HTTP_404_NOT_FOUND
        }
    )

async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Handler for ValidationError.
    Returns 422 status code with error details.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": str(exc),
            "type": "validation_error",
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    )

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    General exception handler for unexpected errors.
    Returns 500 status code with error details.
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "type": "internal_server_error",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )
