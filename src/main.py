from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.infrastructure.api.router import router
from src.infrastructure.api.error_handlers import (
    TaskNotFoundError,
    ValidationError,
    task_not_found_handler,
    validation_error_handler,
    general_exception_handler,
)

app = FastAPI(
    title="TaskFlow Architect",
    description="A modern, clean-architecture approach to task management built with Python and FastAPI",
    version="1.0.0",
)

app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(router)


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")
