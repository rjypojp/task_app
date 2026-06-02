import os
import pytest
from app import app
from database import init_db
import threading
import uuid
import psycopg2


@pytest.fixture
def client():
    app.config["TESTING"] = True    
    
    with app.test_client() as client:
        
        yield client
        
@pytest.fixture(autouse=True)
def setup_db(): 
    with app.app_context():
        init_db()
        yield


def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_task_create(client):
    response = client.post(
        "/", 
        data={
            "title": "テストタスク",
            "deadline": "2026-01-01",
            "comment": ""
      },
      follow_redirects=False
    )

    assert response.status_code == 302


def test_empty_title(client):
    client.post("/register", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)

    client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)
    
    response = client.post("/", data={
        "title": "",
        "deadline": "2026-01-01",
        "comment": ""
    }, follow_redirects=True)
    
    assert "タイトルを入力してください。".encode("utf-8") in response.data
    
def test_login_fail(client):
    response = client.post("/login", data={
        "username": "no_user",
        "password": "wrong_password"
    })
    
    assert response.status_code == 302
    
def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302
    
def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200
    
def test_login_success(client):
    
    from database import create_user
    from werkzeug.security import generate_password_hash
    
    username = f"testuser_{uuid.uuid4()}"
    
    try:
        with app.app_context():
            create_user(
                username,
                generate_password_hash("password123")
            )
    except psycopg2.IntegrityError:
        pass
    
    response = client.post("/login", data={
        "username": username,
        "password": "password123"
    })
    
    assert response.status_code ==302

def test_register_duplicate_user(client):
    client.post("/register", data={
        "username": "duplicate_user",
        "password": "password123"
    })
    
    response = client.post("/register", data={
        "username": "duplicate_user",
        "password": "pasword123"
    }, follow_redirects=True)
    
    assert "このユーザー名は既に使われています。" in response.data.decode("utf-8")

def test_delete_requires_login(client):
    response = client.get("/delete/1")
    assert response.status_code == 302
    
def test_edit_requires_login(client):
    response = client.get("/edit/1")
    assert response.status_code == 302

def test_toggle_requires_login(client):
    response = client.get("/toggle/1")
    assert response.status_code == 302
    
def test_task_create_requires_login(client):
    response = client.post("/", data={
        "title": "テスト",
        "deadline": "2026-01-01",
        "comment": ""
    })
    
    assert response.status_code ==302

def test_task_create_success(client):
    
    username = f"testuser_{uuid.uuid4()}"
    
    client.post("/register", data={
        "username": username,
        "password": "password123"
    })
    
    client.post("/login", data={
        "username": username,
        "password": "password123"
    })
    
    response = client.post("/", data={
        "title": "テストタスク",
        "deadline": "2026-01-01",
        "comment": "" 
    })
    
    assert response.status_code == 302
    
def test_task_saved_even_if_google_fails(client, monkeypatch):

    # ユーザー作成＆ログイン
    client.post("/register", data={
        "username": "testuser",
        "password": "password123"
    })

    client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })

    # Google連携を強制的に失敗させる
    def fake_get_calendar_service():
        raise Exception("Google API error")

    import google_calendar
    monkeypatch.setattr(
        google_calendar,
        "get_calendar_service",
        fake_get_calendar_service
    )

    # タスク作成
    response = client.post("/", data={
        "title": "Google失敗テスト",
        "deadline": "2026-01-01",
        "comment": ""
    })

    # ★重要：タスクは成功扱い（リダイレクト）
    assert response.status_code == 302
    
def test_concurrent_task_create():

    errors = []

    def create_task(i):

        try:

            with app.test_client() as client:

                username = f"testuser_{uuid.uuid4()}"
                
                client.post("/register", data={
                    "username": username,
                    "password": "password123"
                })

                client.post("/login", data={
                    "username": username,
                    "password": "password123"
                })

                response = client.post("/", data={
                    "title": f"task{i}",
                    "deadline": "2026-01-01",
                    "comment": ""
                })

                assert response.status_code == 302

        except Exception as e:
            errors.append(str(e))

    threads = []

    for i in range(3):
        t = threading.Thread(
            target=create_task,
            args=(i,)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert len(errors) == 0

def test_add_task_empty_title(client):
    
    client.post("/register", data={
        "username": "testuser",
        "password": "password123"
    })
    
    client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })
    
    response = client.post(
        "/",
        data={
            "title": "",
            "deadline": "",
            "comment": ""
        },
        follow_redirects=True
    )
    
    assert "タイトルを入力してください。".encode("utf-8") in response.data