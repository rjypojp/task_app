import json
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
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from utils import require_login, validate_task



OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)
app.config["TESTING"] = False

from database import close_db

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

#アプリ起動時に呼ぶ
with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)