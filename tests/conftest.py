# tests/conftest.py
import pytest
from typing import AsyncGenerator
from src.domain.repositories.task_repository import TaskRepository
from src.infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository
from src.domain.services.task_service import TaskService
from src.infrastructure.logging.logger import Logger, ConsoleLogger
from src.application.controllers.task_controller import TaskController

@pytest.fixture
async def repository() -> AsyncGenerator[TaskRepository, None]:
    repo = InMemoryTaskRepository()
    yield repo

@pytest.fixture
async def logger() -> AsyncGenerator[Logger, None]:
    logger = ConsoleLogger()
    yield logger

@pytest.fixture
async def service(repository: TaskRepository) -> AsyncGenerator[TaskService, None]:
    service = TaskService(repository)
    yield service

@pytest.fixture
async def controller(
    service: TaskService,
    logger: Logger
) -> AsyncGenerator[TaskController, None]:
    controller = TaskController(service, logger)
    yield controller
