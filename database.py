import os
from flask import g
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


DB_NAME = "tasks.db"
DB_PATH = "test.db" if os.getenv("TESTING") else "task.db"
NO_DEADLINE_DAYS = 999
DEFAULT_CITY = "Utsunomiya"



def get_db():
    db = g.get("db")

    if db is None or db.closed != 0:
        db = psycopg2.connect(DATABASE_URL)
        g.db = db
    
    return db
    
def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()
        


def init_db():
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            username TEXT,
            deadline TEXT,
            comment TEXT,
            done INTEGER DEFAULT 0,
            google_event_id TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            city TEXT
        )
    """)
    
    conn.commit()
    
    print("DB 初期化完了！")

def get_tasks(username):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT id, title, deadline, done, comment
        FROM tasks
        WHERE username=%s
        ORDER BY deadline IS NULL, deadline
    """, (username,))
    
    rows = c.fetchall()
    
    tasks = []
    
    today = datetime.today().date()
    
    for row in rows:
        
        id, title, deadline, done, comment = row
        
        if deadline:
            due = datetime.strptime(deadline, "%Y-%m-%d").date()
            days_left = (due - today).days
        else:
            days_left = NO_DEADLINE_DAYS
            
        if done == 1:
            color = "gray"
        elif days_left <= 0:
            color = "red"
        elif days_left <= 3:
            color = "orange"
        else:
            color = "black"
            
        tasks.append({
            "id": id,
            "title": title,
            "deadline": deadline,
            "done": done,
            "comment": comment,
            "color": color
        })  
    
    return tasks

def delete_task(id, username):
    
    conn = get_db()
    c = conn.cursor()
    
    try:
        c.execute(
        "DELETE FROM tasks WHERE id=%s AND username=%s",
        (id,username))
    
        conn.commit()
    
    except Exception:
        conn.rollback()
        raise

def toggle_task(id,username):
    
    conn = get_db()
    c = conn.cursor()

    try:
        c.execute(
        "SELECT done FROM tasks WHERE id=%s AND username=%s", 
        (id, username)
        )
    
        row = c.fetchone()

        if not row:
            return
        
        done = row[0]
        
        new_done = 0 if done else 1
    
        c.execute(
            """
            UPDATE tasks
            SET done=%s
            WHERE id=%s AND username=%s
            """, 
            (new_done, id, username)
        )

        conn.commit()
    
    except Exception:
        conn.rollback()
        raise

def get_task_by_id(id, username):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        SELECT title, deadline, comment, google_event_id
        FROM tasks
        WHERE id=%s AND username=%s
        """,
        (id, username)
    )
    
    task = c.fetchone()
    
    return task

def update_task(id, username, title, deadline, comment):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        UPDATE tasks
        SET title=%s, deadline=%s, comment=%s
        WHERE id=%s AND username=%s
        """,
        (title, deadline, comment, id, username)
    )
    
    conn.commit()
    
def add_task(title, username, deadline, comment, google_event_id=None):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        INSERT INTO tasks
        (title, username, deadline, comment, google_event_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (title, username, deadline, comment, google_event_id)
    )
        
    conn.commit()

def update_city(username, city):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        "UPDATE users SET city=%s WHERE username=%s",
        (city, username)
    )
    
    conn.commit()
    
def get_city(username):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        "SELECT city FROM users WHERE username=%s",
        (username, )
    )
    
    row = c.fetchone()
    
    if row and row[0]:
        return row[0]
    else:
        return DEFAULT_CITY
    
def create_user(username, hashed_password):
    
    conn = get_db()
    c = conn.cursor()
    
    try:
        c.execute("""
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """,(username, hashed_password))
    
        conn.commit()
    
    except Exception:
        conn.rollback()
        raise

def get_user_by_username(username):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        SELECT * FROM users
        WHERE  username=%s
        """,
        (username,)         
    )    
    user = c.fetchone()
    
    return user

def get_google_event_id(id, username):
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        SELECT google_event_id
        FROM tasks
        WHERE id=%s AND username=%s
        """,
        (id, username)
    )
    
    row = c.fetchone()
    
    if row:
        return row[0]
    else:
        return None
    
def delete_all_tasks(username):
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        "DELETE FROM tasks WHERE username=%s",
        (username,)
    )
    conn.commit()