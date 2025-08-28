from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.user import User   # ✅ import directly from models.user


# Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Welcome back!", "success")

            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("student.dashboard"))

        flash("Invalid email or password", "danger")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email", "").strip()
        password = request.form.get("password")
        role = request.form.get("role")

        # check if user already exists
        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for("auth.login"))

        hashed_pw = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_pw, role=role)

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
