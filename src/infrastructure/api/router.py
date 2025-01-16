
# src/infrastructure/api/router.py
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Body
from typing import Dict, Any
from typing import List, Optional
from uuid import UUID
from ...application.controllers.task_controller import TaskController
from .models import CreateTaskRequest, UpdateTaskRequest, TaskResponse
from .dependencies import get_controller
from ...domain.entities.task import TaskStatus

router = APIRouter(
    prefix="/api/v1/tasks",
    tags=["tasks"],
    responses={
        404: {
            "description": "Task not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Task not found"}
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "title"],
                                "msg": "Title must not be empty",
                                "type": "value_error"
                            }
                        ]
                    }
                }
            }
        }
    }
)

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=201,
    summary="Create a new task",
    response_description="The created task",
    responses={
        201: {
            "description": "Task created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Implement new feature",
                        "description": "Add user authentication to the API",
                        "status": "PENDING",
                        "assigned_to": "987fcdeb-51k2-12d3-a456-426614174000",
                        "created_at": "2024-01-16T10:00:00.000Z",
                        "updated_at": "2024-01-16T10:00:00.000Z"
                    }
                }
            }
        }
    }
)
async def create_task(
    request: CreateTaskRequest = Body(
        ...,
        example={
            "title": "Implement new feature",
            "description": "Add user authentication to the API",
            "assigned_to": "987fcdeb-51k2-12d3-a456-426614174000"
        }
    ),
    controller: TaskController = Depends(get_controller)
) -> TaskResponse:
    """
    Create a new task with the provided information.

    - **title**: Task title (1-200 characters)
    - **description**: Task description (1-1000 characters)
    - **assigned_to**: Optional UUID of the user to assign the task to
    """
    try:
        task = await controller.create_task(request.dict())
        return TaskResponse.from_orm(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="List all tasks",
    response_description="List of tasks",
    responses={
        200: {
            "description": "List of tasks retrieved successfully",
            "content": {
                "application/json": {
                    "example": [{
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Implement new feature",
                        "description": "Add user authentication to the API",
                        "status": "IN_PROGRESS",
                        "assigned_to": "987fcdeb-51k2-12d3-a456-426614174000",
                        "created_at": "2024-01-16T10:00:00.000Z",
                        "updated_at": "2024-01-16T10:30:00.000Z"
                    }, {
                        "id": "223e4567-e89b-12d3-a456-426614174000",
                        "title": "Fix bug in login",
                        "description": "Address issue with password reset",
                        "status": "PENDING",
                        "assigned_to": null,
                        "created_at": "2024-01-16T11:00:00.000Z",
                        "updated_at": "2024-01-16T11:00:00.000Z"
                    }]
                }
            }
        }
    }
)
async def list_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    assigned_to: Optional[UUID] = Query(None, description="Filter by assigned user"),
    controller: TaskController = Depends(get_controller)
) -> List[TaskResponse]:
    """
    Retrieve all tasks, with optional filtering by status and assigned user.
    """
    tasks = await controller.list_tasks()
    
    # Apply filters if provided
    if status:
        tasks = [task for task in tasks if task.status == status]
    if assigned_to:
        tasks = [task for task in tasks if task.assigned_to == assigned_to]
        
    return [TaskResponse.from_orm(task) for task in tasks]

@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a specific task",
    response_description="The requested task"
)
async def get_task(
    task_id: UUID = Path(..., description="The ID of the task to retrieve"),
    controller: TaskController = Depends(get_controller)
) -> TaskResponse:
    """
    Retrieve a specific task by its ID.
    """
    try:
        task = await controller.get_task(task_id)
        return TaskResponse.from_orm(task)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    response_description="The updated task"
)
async def update_task(
    request: UpdateTaskRequest,
    task_id: UUID = Path(..., description="The ID of the task to update"),
    controller: TaskController = Depends(get_controller)
) -> TaskResponse:
    """
    Update a specific task by its ID.

    - **title**: Optional new title (1-200 characters)
    - **description**: Optional new description (1-1000 characters)
    - **status**: Optional new status
    - **assigned_to**: Optional new assigned user UUID
    """
    try:
        task = await controller.update_task(task_id, request.dict(exclude_unset=True))
        return TaskResponse.from_orm(task)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.post(
    "/{task_id}/assign/{user_id}",
    response_model=TaskResponse,
    summary="Assign a task to a user",
    response_description="The updated task"
)
async def assign_task(
    task_id: UUID = Path(..., description="The ID of the task to assign"),
    user_id: UUID = Path(..., description="The ID of the user to assign the task to"),
    controller: TaskController = Depends(get_controller)
) -> TaskResponse:
    """
    Assign a task to a specific user.
    """
    try:
        task = await controller.assign_task(task_id, user_id)
        return TaskResponse.from_orm(task)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")

@router.post(
    "/{task_id}/status/{status}",
    response_model=TaskResponse,
    summary="Update task status",
    response_description="The updated task"
)
async def update_task_status(
    task_id: UUID = Path(..., description="The ID of the task to update"),
    status: TaskStatus = Path(..., description="The new status"),
    controller: TaskController = Depends(get_controller)
) -> TaskResponse:
    """
    Update the status of a specific task.
    """
    try:
        task = await controller.update_task(task_id, {"status": status})
        return TaskResponse.from_orm(task)
    except ValueError:
        raise HTTPException(status_code=404, detail="Task not found")