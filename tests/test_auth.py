from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_signup():
    response = client.post(
        "/auth/signup", json={"username": "hohohowar", "password": "h4hehehe"}
    )

    assert response.status_code == 200


def test_login_success():
    response = client.post(
        "/auth/login", json={"username": "ureee", "password": "12345678"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


def test_wrong_password():
    response = client.post(
        "auth/login", json={"username": "ureee", "password": "123456oo"}
    )

    assert response.status_code == 401


def test_logout():
    login_resp = client.post(
        "/auth/login", json={"username": "ureee", "password": "12345678"}
    )

    token = login_resp.json()["access_token"]

    response = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200


def test_token_blacklisted():
    login_resp = client.post(
        "/auth/login", json={"username": "ureee", "password": "12345678"}
    )

    token = login_resp.json()["access_token"]

    repsonse = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})

    assert repsonse.status_code == 200


def test_token_blacklisted_after_logout():
    login_resp = client.post(
        "/auth/login", json={"username": "ureee", "password": "hello"}
    )

    token = login_resp.json()["access_token"]

    client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})

    response = client.get("/todo", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
