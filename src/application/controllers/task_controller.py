# src/application/controllers/task_controller.py
from typing import Optional, List
from uuid import UUID
from ...domain.services.task_service import TaskService
from ...infrastructure.logging.logger import Logger
from ..dtos.task_dto import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO
from ...domain.entities.task import Task

class TaskController:
    def __init__(self, task_service: TaskService, logger: Logger):
        self.task_service = task_service
        self.logger = logger

    async def create_task(self, dto: CreateTaskDTO) -> Task:
        try:
            self.logger.info("Creating new task", {"dto": dto.__dict__})
            return await self.task_service.create_task(
                dto.title,
                dto.description,
                dto.assigned_to
            )
        except Exception as error:
            self.logger.error("Error creating task", error, {"dto": dto.__dict__})
            raise

    async def assign_task(self, task_id: UUID, user_id: UUID) -> Task:
        try:
            self.logger.info("Assigning task", {"task_id": task_id, "user_id": user_id})
            return await self.task_service.assign_task(task_id, user_id)
        except Exception as error:
            self.logger.error(
                "Error assigning task",
                error,
                {"task_id": task_id, "user_id": user_id}
            )
            raise

    async def get_task(self, task_id: UUID) -> Task:
        try:
            self.logger.info("Retrieving task", {"task_id": task_id})
            return await self.task_service.get_task(task_id)
        except Exception as error:
            self.logger.error("Error retrieving task", error, {"task_id": task_id})
            raise

    async def list_tasks(self) -> List[Task]:
        try:
            self.logger.info("Listing all tasks")
            return await self.task_service.list_tasks()
        except Exception as error:
            self.logger.error("Error listing tasks", error)
            raise

    async def update_task(self, task_id: UUID, dto: UpdateTaskDTO) -> Task:
        try:
            self.logger.info("Updating task", {"task_id": task_id, "dto": dto.__dict__})
            task = await self.task_service.get_task(task_id)
            
            if dto.status is not None:
                task.update_status(dto.status)
            if dto.assigned_to is not None:
                task.assign(dto.assigned_to)
            if dto.title is not None and dto.description is not None:
                task.update(dto.title, dto.description)

            await self.task_service.task_repository.save(task)
            return task
        except Exception as error:
            self.logger.error("Error updating task", error, {
                "task_id": task_id,
                "dto": dto.__dict__
            })
            raise
