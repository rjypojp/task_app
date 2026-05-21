import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_login_page():
    client = app.test_client()
    response = client.get("/login")

    assert response.status_code == 200


def test_task_create(client):
    response = client.post("/", data={
        "title": "テストタスク",
        "deadline": "2026-01-01",
        "comment": ""
    })

    assert response.status_code == 302


def test_empty_title(client):
    response = client.post("/", data={
        "title": "",
        "deadline": "2026-01-01",
        "comment": ""
    })

    assert response.status_code == 302