from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db   # ✅ use the same db
from models import User



# Blueprint for authentication routes
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("student.dashboard"))
        else:
            flash("❌ Wrong email or password!", "danger")  # flash only on error

    return render_template("login.html")


@auth_bp.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    from flask_login import current_user

    user = current_user
    user_id = user.id

    # Delete user from DB
    db.session.delete(user)
    db.session.commit()

    logout_user()

    flash("Your account has been deleted successfully.", "info")
    return redirect(url_for("auth.register"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]

        # create new user
        new_user = User(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
