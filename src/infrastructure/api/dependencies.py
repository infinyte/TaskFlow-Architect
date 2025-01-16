# src/infrastructure/api/dependencies.py
from fastapi import Depends
from typing import AsyncGenerator
from ...domain.repositories.task_repository import TaskRepository
from ...domain.services.task_service import TaskService
from ...infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository
from ...infrastructure.logging.logger import Logger, ConsoleLogger
from ...application.controllers.task_controller import TaskController

async def get_repository() -> AsyncGenerator[TaskRepository, None]:
    """
    Dependency provider for TaskRepository.
    Currently using InMemoryTaskRepository, but can be easily switched to another implementation.
    """
    repository = InMemoryTaskRepository()
    yield repository

async def get_logger() -> AsyncGenerator[Logger, None]:
    """
    Dependency provider for Logger.
    """
    logger = ConsoleLogger()
    yield logger

async def get_service(
    repository: TaskRepository = Depends(get_repository)
) -> AsyncGenerator[TaskService, None]:
    """
    Dependency provider for TaskService.
    """
    service = TaskService(repository)
    yield service

async def get_controller(
    service: TaskService = Depends(get_service),
    logger: Logger = Depends(get_logger)
) -> AsyncGenerator[TaskController, None]:
    """
    Dependency provider for TaskController.
    """
    controller = TaskController(service, logger)
    yield controller