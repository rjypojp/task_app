import json
import sqlite3
from flask import Flask, render_template, request
from flask import redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import ( 
     get_tasks,
     delete_task,
     toggle_task,
     get_task_by_id,
     update_task,
     add_task,
     update_city,
     get_city,
     create_user,
     get_user_by_username,
     init_db,
     get_google_event_id
)
from weather import get_weather
from holiday import get_holidays
from calendar_utils import create_events
from google_calendar import add_event, update_event, delete_event
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

#データベース作成とtasksテーブル作成

def require_login():
    
    if "user" not in session:
        return None
    
    return session["user"]

#アプリ起動時に呼ぶ
init_db()

@app.route("/", methods=["GET", "POST"])
def index():

    # =========================
    # ログイン確認
    # =========================
    user = require_login()
    
    if not user:
        return redirect(url_for("login"))
    
    # =========================
    # 都市設定の取得・保存
    # =========================
    input_city = request.values.get("city", "").strip()
    
    if input_city:
        update_city(user, input_city)
    else:
        input_city = get_city(user)
        
    # =========================
    # タスク追加
    # =========================
    if request.method == "POST":
        title = request.form["title"]
        deadline = request.form["deadline"]
        comment = request.form["comment"]
        
        event_id = None
        
        if deadline:
            event_id = add_event(title, deadline)
        
        add_task(
            title,
            user,
            deadline,
            comment,
            event_id
        )
    
        return redirect(url_for("index"))
    
    # =========================
    # 天気情報取得
    # =========================
    weather, temp, weather_list = get_weather(
        input_city,
        OPENWEATHER_API_KEY
    )
    
    # =========================
    # タスク取得
    # =========================
    tasks = get_tasks(user)
    
    
    # =========================
    # カレンダーイベント作成
    # =========================
    events = create_events(tasks)
    holidays = get_holidays()
    
    # =========================
    # 画面表示
    # =========================
    return render_template(
        "index.html",
        tasks=tasks,
        user=user,
        events=events + holidays,
        weather=weather,
        temp=temp,
        weather_list=weather_list,
        city=input_city
    )

@app.route("/delete/<int:id>")
def delete(id):

    user = require_login()
    
    if not user:
        return redirect(url_for("login"))
    
    event_id = get_google_event_id(id, user)
    
    if event_id:
        delete_event(event_id)
    
    delete_task(id, user)
    
    return redirect(url_for("index"))
   
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    user = require_login()
    
    if not user:
        return redirect(url_for("login"))
    

    if request.method == "POST":
        new_title = request.form["title"]
        new_deadline = request.form["deadline"]
        new_comment = request.form["comment"]
        
        task = get_task_by_id(id, user)
        event_id = task[3]

        update_task(
            id,
            user,
            new_title,
            new_deadline,
            new_comment
        )

        if event_id and new_deadline:
            update_event(event_id, new_title, new_deadline)
        
        return redirect(url_for("index"))
    
    task = get_task_by_id(id, user)
    
    if task:
        return render_template(
            "edit.html", 
            id=id, 
            task=task[0],
            deadline=task[1],
            comment=task[2]
        )
    else:
        return redirect(url_for("index"))
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)
        
        try:
            create_user(username, hashed_password)
            return redirect(url_for("index"))
        
        except sqlite3.IntegrityError:
            return "このユーザー名は既に使われています。"
        
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login(): 
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)

     
        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect(url_for("index"))
            
        flash("ユーザー名またはパスワードが違います。")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/toggle/<int:id>")
def toggle(id):

    user = require_login()
    
    if not user:
        return redirect(url_for("login"))
    
    
    toggle_task(id, user)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)