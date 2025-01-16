# src/domain/repositories/task_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ..entities.task import Task

class TaskRepository(ABC):
    @abstractmethod
    async def save(self, task: Task) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Optional[Task]:
        pass

    @abstractmethod
    async def find_all(self) -> List[Task]:
        pass

    @abstractmethod
    async def find_by_assignee(self, user_id: UUID) -> List[Task]:
        pass

    @abstractmethod
    async def delete(self, id: UUID) -> None:
        pass

