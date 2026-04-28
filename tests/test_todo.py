from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_todo():
    login = client.post(
        "/auth/login", json={"username": "developer", "password": "12345678"}
    )

    token = login.json()["access_token"]

    response = client.post(
        "/todo/post",
        json={"todo_text": "Doing homework", "is_completed": True},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_get_todo():
    login = client.post(
        "/auth/login", json={"username": "developer", "password": "12345678"}
    )

    token = login.json()["access_token"]

    response = client.get("/todo/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200


def test_update_todo():
    login = client.post(
        "/auth/login", json={"username": "developer", "password": "12345678"}
    )

    token = login.json()["access_token"]

    response = client.patch(
        "/todo/22",
        json={"todo_text": "Take exam"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_delete_todo():
    login = client.post(
        "/auth/login", json={"username": "developer", "password": "12345678"}
    )

    token = login.json()["access_token"]

    response = client.delete("/todo/22", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

def test_delete_todo_available():
    login = client.post(
        "/auth/login", json={"username": "developer", "password": "12345678"}
    )

    token = login.json()["access_token"]

    response = client.delete("/todo/22", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 404