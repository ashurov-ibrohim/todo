from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_signup():
    response = client.post(
        "/auth/signup", json={"username": "developer", "password": "12345678"}
    )

    assert response.status_code == 200


def test_login_success():
    response = client.post(
        "/auth/login", json={"username": "developer", "password": "12345678"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


def test_wrong_password():
    response = client.post(
        "/auth/login", json={"username": "ureee", "password": "123456oo"}
    )

    assert response.status_code == 401


def test_logout():
    data = client.post(
        "/auth/login", json={"username": "ureee", "password": "12345678"}
    )

    token = data.json()["access_token"]

    response = client.post('/auth/logout', headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200

def test_logout_blacklisted_tokens():
    data = client.post(
        "/auth/login", json={"username": "ureee", "password": "12345678"}
    )
    token = data.json()["access_token"]

    logout = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})

    response = client.get(
        "/todo/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401