import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for

from routes.auth import auth_bp
from routes.tasks import tasks_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

@app.route("/")
def home():
    return redirect(url_for("auth.login"))

if __name__ == "__main__":
    app.run(debug=True)