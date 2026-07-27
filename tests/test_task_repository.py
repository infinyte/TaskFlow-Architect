# tests/test_task_repository.py
import pytest
from uuid import uuid4
from src.domain.entities.task import Task, TaskStatus
from src.infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository


@pytest.fixture
def repo():
    return InMemoryTaskRepository()


async def test_save_and_find_by_id(repo):
    task = Task.create("Test task", "Description")
    await repo.save(task)
    found = await repo.find_by_id(task.id)
    assert found is not None
    assert found.id == task.id


async def test_find_by_id_returns_none_when_missing(repo):
    result = await repo.find_by_id(uuid4())
    assert result is None


async def test_find_all_returns_all_saved_tasks(repo):
    task1 = Task.create("Task 1", "Desc 1")
    task2 = Task.create("Task 2", "Desc 2")
    await repo.save(task1)
    await repo.save(task2)
    all_tasks = await repo.find_all()
    assert len(all_tasks) == 2


async def test_find_all_empty_repository(repo):
    all_tasks = await repo.find_all()
    assert all_tasks == []


async def test_save_overwrites_existing_task(repo):
    task = Task.create("Original", "Desc")
    await repo.save(task)
    task.update("Updated", "Updated desc")
    await repo.save(task)
    found = await repo.find_by_id(task.id)
    assert found.title == "Updated"


async def test_delete_removes_task(repo):
    task = Task.create("To delete", "Desc")
    await repo.save(task)
    await repo.delete(task.id)
    found = await repo.find_by_id(task.id)
    assert found is None


async def test_delete_nonexistent_task_does_not_raise(repo):
    await repo.delete(uuid4())  # should not raise


async def test_find_by_assignee_returns_matching_tasks(repo):
    user_id = uuid4()
    task1 = Task.create("Task 1", "Desc", assigned_to=user_id)
    task2 = Task.create("Task 2", "Desc", assigned_to=uuid4())
    task3 = Task.create("Task 3", "Desc", assigned_to=user_id)
    await repo.save(task1)
    await repo.save(task2)
    await repo.save(task3)
    results = await repo.find_by_assignee(user_id)
    assert len(results) == 2
    assert all(t.assigned_to == user_id for t in results)


async def test_find_by_assignee_returns_empty_when_none_match(repo):
    task = Task.create("Task", "Desc", assigned_to=uuid4())
    await repo.save(task)
    results = await repo.find_by_assignee(uuid4())
    assert results == []
