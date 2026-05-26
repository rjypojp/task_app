from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


from database import (
    create_user,
    get_user_by_username
)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login(): 
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = get_user_by_username(username)

     
        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect(url_for("tasks.index"))
            
        flash("ユーザー名またはパスワードが違います。")
        return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if not username:
            flash("ユーザー名を入力してください。")
            return redirect(url_for("auth.register"))

        if len(password) <8:
            flash("パスワードは8文字以上にしてください。")
            return redirect(url_for("auth.register"))
        
        hashed_password = generate_password_hash(password)
        
        try:
            create_user(username, hashed_password)
            return redirect(url_for("tasks.index"))
        
        except sqlite3.IntegrityError:
            return "このユーザー名は既に使われています。"
        
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("auth.login"))