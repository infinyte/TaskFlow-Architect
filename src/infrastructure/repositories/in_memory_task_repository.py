# src/infrastructure/repositories/in_memory_task_repository.py
from typing import Dict, List, Optional
from uuid import UUID
from ...domain.entities.task import Task
from ...domain.repositories.task_repository import TaskRepository

class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks: Dict[UUID, Task] = {}

    async def save(self, task: Task) -> None:
        self.tasks[task.id] = task

    async def find_by_id(self, id: UUID) -> Optional[Task]:
        return self.tasks.get(id)

    async def find_all(self) -> List[Task]:
        return list(self.tasks.values())

    async def find_by_assignee(self, user_id: UUID) -> List[Task]:
        return [task for task in self.tasks.values() if task.assigned_to == user_id]

    async def delete(self, id: UUID) -> None:
        self.tasks.pop(id, None)
