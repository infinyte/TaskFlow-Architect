# src/infrastructure/api/models.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from ...domain.entities.task import TaskStatus

class CreateTaskRequest(BaseModel):
    """
    Model for creating a new task.

    Example:
        ```json
        {
            "title": "Implement new feature",
            "description": "Add user authentication to the API",
            "assigned_to": "987fcdeb-51k2-12d3-a456-426614174000"
        }
        ```
    """
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Implement new feature",
                "description": "Add user authentication to the API",
                "assigned_to": "987fcdeb-51k2-12d3-a456-426614174000"
            }
        }
    }
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(..., min_length=1, max_length=1000, description="Task description")
    assigned_to: Optional[UUID] = Field(None, description="UUID of the assigned user")

    @validator('title')
    def title_must_not_be_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Title must not be empty')
        return v

    @validator('description')
    def description_must_not_be_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Description must not be empty')
        return v

class UpdateTaskRequest(BaseModel):
    """
    Model for updating an existing task.

    Example:
        ```json
        {
            "title": "Updated feature implementation",
            "description": "Add OAuth2 authentication to the API",
            "status": "IN_PROGRESS",
            "assigned_to": "987fcdeb-51k2-12d3-a456-426614174000"
        }
        ```
    """
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Updated feature implementation",
                "description": "Add OAuth2 authentication to the API",
                "status": "IN_PROGRESS",
                "assigned_to": "987fcdeb-51k2-12d3-a456-426614174000"
            }
        }
    }
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    status: Optional[TaskStatus] = Field(None)
    assigned_to: Optional[UUID] = Field(None)

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Title must not be empty')
        return v

    @validator('description')
    def description_must_not_be_empty(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError('Description must not be empty')
        return v

class TaskResponse(BaseModel):
    """
    Model for task response data.
    """
    id: UUID
    title: str
    description: str
    status: TaskStatus
    assigned_to: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
