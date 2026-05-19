import sqlite3
from datetime import datetime

DB_NAME = "tasks.db"
NO_DEADLINE_DAYS = 999
DEFAULT_CITY = "Utsunomiya"



def get_db():
    
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            user TEXT,
            deadline TEXT,
            comment TEXT,
            done INTEGER DEFAULT 0,
            google_event_id TEXT
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            city TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    
    print("DB 初期化完了！")

def get_tasks(user):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""
        SELECT id, title, deadline, done, comment
        FROM tasks
        WHERE user=?
        ORDER BY deadline IS NULL, deadline
    """, (user,))
    
    rows = c.fetchall()
    
    conn.close()
    
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

def delete_task(id, user):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        "DELETE FROM tasks WHERE id=? AND user=?",
        (id,user)
    )
    
    conn.commit()
    conn.close()

def toggle_task(id,user):
    
    conn = get_db()
    c = conn.cursor()

    c.execute(
        "SELECT done FROM tasks WHERE id=? AND user=?", 
        (id, user)
    )
    
    row = c.fetchone()

    if row:
        
        done = row[0]
        
        new_done = 0 if done else 1
    
        c.execute(
            """
            UPDATE tasks
            SET done=?
            WHERE id=? AND user=?
            """, 
            (new_done, id, user)
        )

    conn.commit()
    conn.close()

def get_task_by_id(id, user):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        SELECT title, deadline, comment, google_event_id
        FROM tasks
        WHERE id=? AND user=?
        """,
        (id, user)
    )
    
    task = c.fetchone()
    
    conn.close()
    
    return task

def update_task(id, user, title, deadline, comment):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        UPDATE tasks
        SET title=?, deadline=?, comment=?
        WHERE id=? AND user=?
        """,
        (title, deadline, comment, id, user)
    )
    
    conn.commit()
    conn.close()
    
def add_task(title, user, deadline, comment, google_event_id=None):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        INSERT INTO tasks
        (title, user, deadline, comment, google_event_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (title, user, deadline, comment, google_event_id)
    )
        
    conn.commit()
    conn.close()

def update_city(user, city):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        "UPDATE users SET city=? WHERE username=?",
        (city, user)
    )
    
    conn.commit()
    conn.close()
    
def get_city(user):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        "SELECT city FROM users WHERE username=?",
        (user, )
    )
    
    row = c.fetchone()
    
    conn.close()
    
    if row and row[0]:
        return row[0]
    else:
        return DEFAULT_CITY
    
def create_user(username, hashed_password):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        INSERT INTO users (username, password)
        VALUES (?, ?)
        """,
        (username, hashed_password)
    )
    
    conn.commit()
    conn.close()

def get_user_by_username(username):
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        SELECT * FROM users
        WHERE  username=?
        """,
        (username,)         
    )    
    user = c.fetchone()
    
    conn.close()
    
    return user

def get_google_event_id(id, user):
    conn = get_db()
    c = conn.cursor()
    
    c.execute(
        """
        SELECT google_event_id
        FROM tasks
        WHERE id=? AND user=?
        """,
        (id, user)
    )
    
    row = c.fetchone()
    
    conn.close()
    
    if row:
        return row[0]
    else:
        return None