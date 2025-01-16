# src/domain/entities/task.py
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4
from typing import Optional

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

@dataclass
class Task:
    id: UUID
    title: str
    description: str
    status: TaskStatus
    assigned_to: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, title: str, description: str, assigned_to: Optional[UUID] = None) -> "Task":
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            assigned_to=assigned_to,
            created_at=now,
            updated_at=now
        )

    def assign(self, user_id: UUID) -> None:
        self.assigned_to = user_id
        self.updated_at = datetime.utcnow()

    def update_status(self, status: TaskStatus) -> None:
        self.status = status
        self.updated_at = datetime.utcnow()

    def update(self, title: str, description: str) -> None:
        self.title = title
        self.description = description
        self.updated_at = datetime.utcnow()