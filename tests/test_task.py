from app import app
from database import add_task, get_tasks, delete_task

def test_add_task():
    
    with app.app_context():
        
        add_task(
            "テストタスク",
            "testuser",
            "2026-01-01",
            "memo"
        )
    
        tasks = get_tasks("testuser")
    
        assert len(tasks) > 0
    
        assert any(t["title"] == "テストタスク" for t in tasks)

def test_delete_task():
    
    with app.app_context():
        
        add_task("削除テスト",
                "testuser",
                "2026-01-01",
                "memo"
        )
    
        tasks = get_tasks("testuser")
        task_id = tasks[-1]["id"]
    
        delete_task(task_id, "testuser")
    
        tasks_after = get_tasks("testuser")
    
        assert all(t["id"] != task_id for t in tasks_after)    
    