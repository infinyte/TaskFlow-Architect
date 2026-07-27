# tests/test_task_entity.py
import pytest
from uuid import uuid4
from src.domain.entities.task import Task, TaskStatus


def test_create_sets_pending_status():
    task = Task.create("Fix bug", "Details here")
    assert task.status == TaskStatus.PENDING


def test_create_assigns_uuid():
    task = Task.create("Fix bug", "Details here")
    assert task.id is not None


def test_create_sets_timestamps():
    task = Task.create("Fix bug", "Details here")
    assert task.created_at is not None
    assert task.updated_at is not None
    assert task.created_at == task.updated_at


def test_create_with_assignee():
    user_id = uuid4()
    task = Task.create("Fix bug", "Details here", assigned_to=user_id)
    assert task.assigned_to == user_id


def test_create_without_assignee():
    task = Task.create("Fix bug", "Details here")
    assert task.assigned_to is None


def test_assign_updates_assigned_to():
    task = Task.create("Fix bug", "Details here")
    user_id = uuid4()
    task.assign(user_id)
    assert task.assigned_to == user_id


def test_assign_updates_updated_at():
    task = Task.create("Fix bug", "Details here")
    original_updated_at = task.updated_at
    task.assign(uuid4())
    assert task.updated_at >= original_updated_at


def test_update_status_changes_status():
    task = Task.create("Fix bug", "Details here")
    task.update_status(TaskStatus.IN_PROGRESS)
    assert task.status == TaskStatus.IN_PROGRESS


def test_update_status_updates_updated_at():
    task = Task.create("Fix bug", "Details here")
    original_updated_at = task.updated_at
    task.update_status(TaskStatus.COMPLETED)
    assert task.updated_at >= original_updated_at


def test_update_changes_title_and_description():
    task = Task.create("Old title", "Old description")
    task.update("New title", "New description")
    assert task.title == "New title"
    assert task.description == "New description"


def test_update_updates_updated_at():
    task = Task.create("Old title", "Old description")
    original_updated_at = task.updated_at
    task.update("New title", "New description")
    assert task.updated_at >= original_updated_at
