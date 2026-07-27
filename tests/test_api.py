# tests/test_api.py
import pytest
from uuid import uuid4
from httpx import AsyncClient, ASGITransport
from src.main import app


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


async def test_root_redirects_to_docs(client):
    response = await client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


async def test_create_task_returns_201(client):
    response = await client.post(
        "/api/v1/tasks/",
        json={"title": "Test task", "description": "Test description"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert data["status"] == "PENDING"
    assert data["assigned_to"] is None
    assert "id" in data


async def test_create_task_with_assignee(client):
    user_id = str(uuid4())
    response = await client.post(
        "/api/v1/tasks/",
        json={
            "title": "Assigned task",
            "description": "Some description",
            "assigned_to": user_id,
        },
    )
    assert response.status_code == 201
    assert response.json()["assigned_to"] == user_id


async def test_create_task_rejects_empty_title(client):
    response = await client.post(
        "/api/v1/tasks/",
        json={"title": "   ", "description": "Some description"},
    )
    assert response.status_code == 422


async def test_create_task_rejects_missing_fields(client):
    response = await client.post("/api/v1/tasks/", json={})
    assert response.status_code == 422


async def test_list_tasks_returns_empty_list(client):
    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 200
    assert response.json() == []


async def test_list_tasks_returns_created_tasks(client):
    await client.post(
        "/api/v1/tasks/",
        json={"title": "Task A", "description": "Desc A"},
    )
    await client.post(
        "/api/v1/tasks/",
        json={"title": "Task B", "description": "Desc B"},
    )
    response = await client.get("/api/v1/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_task_returns_task(client):
    create = await client.post(
        "/api/v1/tasks/",
        json={"title": "Get me", "description": "Desc"},
    )
    task_id = create.json()["id"]
    response = await client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


async def test_get_task_returns_404_for_unknown_id(client):
    response = await client.get(f"/api/v1/tasks/{uuid4()}")
    assert response.status_code == 404


async def test_update_task_changes_status(client):
    create = await client.post(
        "/api/v1/tasks/",
        json={"title": "Update me", "description": "Desc"},
    )
    task_id = create.json()["id"]
    response = await client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": "IN_PROGRESS"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"


async def test_update_task_returns_404_for_unknown_id(client):
    response = await client.patch(
        f"/api/v1/tasks/{uuid4()}",
        json={"status": "IN_PROGRESS"},
    )
    assert response.status_code == 404


async def test_assign_task_updates_assigned_to(client):
    create = await client.post(
        "/api/v1/tasks/",
        json={"title": "Assign me", "description": "Desc"},
    )
    task_id = create.json()["id"]
    user_id = str(uuid4())
    response = await client.post(f"/api/v1/tasks/{task_id}/assign/{user_id}")
    assert response.status_code == 200
    assert response.json()["assigned_to"] == user_id


async def test_assign_task_returns_404_for_unknown_id(client):
    response = await client.post(f"/api/v1/tasks/{uuid4()}/assign/{uuid4()}")
    assert response.status_code == 404
