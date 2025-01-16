# src/application/dtos/task_dto.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID
from ...domain.entities.task import TaskStatus

@dataclass
class CreateTaskDTO:
    title: str
    description: str
    assigned_to: Optional[UUID] = None

@dataclass
class UpdateTaskDTO:
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    assigned_to: Optional[UUID] = None

@dataclass
class TaskResponseDTO:
    id: UUID
    title: str
    description: str
    status: TaskStatus
    assigned_to: Optional[UUID]
    created_at: datetime
    updated_at: datetime
