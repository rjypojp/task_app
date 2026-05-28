from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    current_app
)

from database import (
    get_tasks,
    add_task,
    update_city,
    get_city,
    get_google_event_id,
    delete_task,
    toggle_task,
    get_task_by_id,
    update_task
)

from weather import get_weather
from holiday import get_holidays
from calendar_utils import create_events

# from google_calendar import (
#     add_event,
#     update_event,
#     delete_event
# )
import os

from utils import require_login, validate_task

tasks_bp = Blueprint("tasks", __name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


@tasks_bp.route("/", methods=["GET", "POST"])
def index():

    # =========================
    # ログイン確認
    # =========================
    user = require_login()
    
    if not user:
        return redirect(url_for("auth.login"))
    
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
        title = request.form["title"].strip()
        deadline = request.form["deadline"].strip()
        comment = request.form["comment"].strip()
        
        error = validate_task(title, comment)
        
        if error:
            flash(error)
            return redirect(url_for("tasks.index"))
        
        event_id = None
        
        # if deadline and not current_app.config.get("TESTING"):
        #     event_id = add_event(title, deadline)
        
        add_task(
            title,
            user,
            deadline,
            comment,
            event_id
        )
        return redirect(url_for("tasks.index"))
    
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

@tasks_bp.route("/delete/<int:id>")
def delete(id):

    user = require_login()
    
    if not user:
        return redirect(url_for("auth.login"))
    
    event_id = get_google_event_id(id, user)
    
    if event_id:
        # delete_event(event_id)
    
        pass
    
    return redirect(url_for("tasks.index"))
   
@tasks_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    user = require_login()
    
    if not user:
        return redirect(url_for("auth.login"))
    

    if request.method == "POST":
        new_title = request.form["title"].strip()
        new_deadline = request.form["deadline"].strip()
        new_comment = request.form["comment"].strip()
        
        error = validate_task(new_title, new_comment)
        
        if error:
            flash(error)
            return redirect(url_for("edit", id=id))
        
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
            # update_event(event_id, new_title, new_deadline)
        
            pass
    
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
        return redirect(url_for("tasks.index"))

@tasks_bp.route("/toggle/<int:id>")
def toggle(id):

    user = require_login()
    
    if not user:
        return redirect(url_for("auth.login"))
    
    
    toggle_task(id, user)

    return redirect(url_for("tasks.index"))