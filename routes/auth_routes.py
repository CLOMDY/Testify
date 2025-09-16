from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db   # ✅ use the same db
from models import User
import uuid


# Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):  # ✅ use method in User model
            login_user(user)

            # Redirect based on role
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("student.dashboard"))

        flash("Invalid email or password", "danger")

    return render_template("login.html")


@auth_bp.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    from flask_login import current_user

    user = current_user

    db.session.delete(user)
    db.session.commit()

    logout_user()
    flash("Your account has been deleted successfully.", "info")
    return redirect(url_for("auth.register"))




@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        # 🔴 Prevent duplicate emails
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("⚠️ This email is already registered.", "warning")
            return redirect(url_for("auth.register"))

        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)

        if role == "admin":
            # ✅ generate a permanent teacher key
            new_user.teacher_key = str(uuid.uuid4())[:8]

        elif role == "student":
            teacher_key = request.form.get("teacher_key")
            teacher = User.query.filter_by(teacher_key=teacher_key, role="admin").first()

            if not teacher:
                flash("❌ Invalid teacher key!", "danger")
                return redirect(url_for("auth.register"))

            # ✅ link student with admin
            new_user.teacher_id = teacher.id

        db.session.add(new_user)
        db.session.commit()

        # ✅ log the user in immediately after registration
        login_user(new_user)

        # ✅ redirect based on role
        if role == "admin":
            return redirect(url_for("admin.dashboard"))
        else:
            return redirect(url_for("student.dashboard"))

    return render_template("register.html")


@auth_bp.route("/check-email", methods=["POST"])
def check_email():
    email = request.json.get("email")
    if not email:
        return {"exists": False}

    exists = User.query.filter_by(email=email).first() is not None
    return {"exists": exists}

@auth_bp.route("/check-teacher-key", methods=["POST"])
def check_teacher_key():
    key = request.json.get("teacher_key")
    if not key:
        return {"valid": False}

    teacher = User.query.filter_by(teacher_key=key, role="admin").first()
    return {"valid": teacher is not None}



@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
