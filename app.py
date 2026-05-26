from flask import Flask, redirect, url_for
from routes.auth import auth_bp
from routes.tasks import tasks_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

@app.route("/")
def hello():
    return redirect(url_for("auth.login"))