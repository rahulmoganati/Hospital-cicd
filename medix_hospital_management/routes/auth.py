from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models import User
bp = Blueprint("auth", __name__)
@bp.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("main.index"))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email","").strip().lower(), is_active=True).first()
        if user and user.check_password(request.form.get("password","")):
            login_user(user); flash("Welcome back.","success"); return redirect(url_for("main.index"))
        flash("Email or password is incorrect.","danger")
    return render_template("auth/login.html")
@bp.route("/logout", methods=["POST"])
def logout():
    logout_user(); return redirect(url_for("auth.login"))
