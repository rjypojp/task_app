import os

os.environ["TESTING"] = "1"

from playwright.sync_api import sync_playwright
from tests.test_utils import start_server


def test_login_page():
    
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True)
        
        page = browser.new_page()
        
        page.goto("http://127.0.0.1:5000/login")
        
        assert "ログイン" in page.content()
        
        browser.close()
        
def test_login():
    start_server()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000/login")
        
        page.fill('input[name="username"]', "testuser")
        page.fill('input[name="password"]', "password123")
        
        page.click('button[type="submit"]')
        
        page.wait_for_load_state("networkidle")
        
        assert "タスク管理アプリ" in page.content()
        
        browser.close()
        
def test_add_task():
    
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True)
        
        page = browser.new_page()
        
        page.goto("http://127.0.0.1:5000/login")
        
        page.fill('input[name="username"]', "testuser")
        page.fill('input[name="password"]', "password123")
        
        page.click('button[type="submit"]')
        
        page.wait_for_load_state("networkidle")
        
        page.fill('input[name="title"]', "Playwrightテスト")
        
        page.fill('input[name="deadline"]', "2026-12-31")
        
        page.fill('input[name="comment"]', "E2Eテスト")
        
        page.click('button[type="submit"]')
        
        page.wait_for_load_state("networkidle")
        
        assert "Playwrightテスト" in page.content()
        
        browser.close()
        
def test_delete_task():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        #ログイン
        page.goto("http://127.0.0.1:5000/login")
        page.fill('input[name="username"]', "testuser")
        page.fill('input[name="password"]', "password123")
        page.click('button[type="submit"]')
        
        page.wait_for_load_state("networkidle")
        
        #ダイアログOK
        page.on("dialog", lambda dialog: dialog.accept())
        
        #タスク追加(削除対象を作る)
        page.fill('input[name="title"]', "削除テスト")
        page.fill('input[name="deadline"]', "2026-12-31")
        page.fill('input[name="comment"]', "E2E")
        page.click('button[type="submit"]')
        
        page.wait_for_load_state("networkidle")
        
        #カードを特定して削除
        card = page.locator(".card", has_text="削除テスト").last
        
        delete_button = card.locator("a", has_text="削除").first
        delete_button.click()
        
        #消えるまで待つ
        
        card.wait_for(state="detached")
        
        #消えたか確認
        assert "削除テスト" not in page.content()
        
        browser.close()
        
def test_edit_task():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # ログイン
        page.goto("http://127.0.0.1:5000/login")
        page.fill('input[name="username"]', "testuser")
        page.fill('input[name="password"]', "password123")
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")

        # タスク作成（編集対象）
        page.fill('input[name="title"]', "編集前タイトル")
        page.fill('input[name="deadline"]', "2026-12-31")
        page.fill('input[name="comment"]', "E2E")
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")

        # 編集対象カードを安定取得
        card = page.locator(".card", has_text="編集前タイトル").first
        
        # 編集ボタン (安定セレクタ)
        edit_btn = card.locator("a:has-text('編集')")
        edit_btn.click()
        
        # 編集画面へ遷移確認
        
        page.wait_for_url("**/edit/**")
        page.wait_for_load_state("domcontentloaded")
        
        # 編集処理
        page.fill('input[name="title"]', "編集後タイトル")
        page.fill('input[name="comment"]', "変更済み")
        page.click('button[type="submit"]')
        
        page.wait_for_load_state("domcontentloaded")
        
        # 反映確認
        assert "編集後タイトル" in page.content()
        
        browser.close()
        
def test_task_list():
    start_server()
    
    from database import delete_all_tasks
    from app import app
    
    with app.app_context():
        delete_all_tasks("testuser")
               
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # ログイン
        page.goto("http://127.0.0.1:5000/login")
        page.fill('input[name="username"]', "testuser")
        page.fill('input[name="password"]', "password123")
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")
        
        # タスク作成（一覧確認用）
        page.fill('input[name="title"]', "一覧テストタスク999")
        page.fill('input[name="deadline"]', "2026-12-31")
        page.fill('input[name="comment"]', "LIST")
        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")

        assert page.locator(
            ".card", 
            has_text="一覧テストタスク999"
        ).count() == 1
        
        browser.close()
    