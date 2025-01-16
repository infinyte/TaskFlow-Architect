# src/domain/services/task_service.py
from typing import Optional, List
from uuid import UUID
from ..entities.task import Task, TaskStatus
from ..repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def create_task(
        self, title: str, description: str, assigned_to: Optional[UUID] = None
    ) -> Task:
        task = Task.create(title, description, assigned_to)
        await self.task_repository.save(task)
        return task

    async def assign_task(self, task_id: UUID, user_id: UUID) -> Task:
        task = await self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        task.assign(user_id)
        await self.task_repository.save(task)
        return task

    async def update_task_status(self, task_id: UUID, status: TaskStatus) -> Task:
        task = await self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError("Task not found")

        task.update_status(status)
        await self.task_repository.save(task)
        return task

    async def get_task(self, task_id: UUID) -> Task:
        task = await self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        return task

    async def list_tasks(self) -> List[Task]:
        return await self.task_repository.find_all()
