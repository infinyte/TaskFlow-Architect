# tests/test_task_service.py
import pytest
from uuid import uuid4
from src.domain.entities.task import TaskStatus
from src.domain.services.task_service import TaskService
from src.infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository


@pytest.fixture
def service():
    return TaskService(InMemoryTaskRepository())


async def test_create_task_returns_task(service):
    task = await service.create_task("My task", "Description")
    assert task.title == "My task"
    assert task.description == "Description"
    assert task.status == TaskStatus.PENDING


async def test_create_task_persists_to_repository(service):
    task = await service.create_task("My task", "Description")
    fetched = await service.get_task(task.id)
    assert fetched.id == task.id


async def test_create_task_with_assignee(service):
    user_id = uuid4()
    task = await service.create_task("My task", "Description", assigned_to=user_id)
    assert task.assigned_to == user_id


async def test_get_task_raises_when_not_found(service):
    with pytest.raises(ValueError, match="Task not found"):
        await service.get_task(uuid4())


async def test_list_tasks_returns_all(service):
    await service.create_task("Task 1", "Desc 1")
    await service.create_task("Task 2", "Desc 2")
    tasks = await service.list_tasks()
    assert len(tasks) == 2


async def test_list_tasks_empty(service):
    tasks = await service.list_tasks()
    assert tasks == []


async def test_assign_task_updates_assignee(service):
    task = await service.create_task("My task", "Description")
    user_id = uuid4()
    updated = await service.assign_task(task.id, user_id)
    assert updated.assigned_to == user_id


async def test_assign_task_raises_when_not_found(service):
    with pytest.raises(ValueError, match="Task not found"):
        await service.assign_task(uuid4(), uuid4())


async def test_update_task_status_changes_status(service):
    task = await service.create_task("My task", "Description")
    updated = await service.update_task_status(task.id, TaskStatus.IN_PROGRESS)
    assert updated.status == TaskStatus.IN_PROGRESS


async def test_update_task_status_raises_when_not_found(service):
    with pytest.raises(ValueError, match="Task not found"):
        await service.update_task_status(uuid4(), TaskStatus.COMPLETED)
