from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin_dashboard.html", user=current_user)

@admin_bp.route("/manage-students")
@login_required
def manage_students():
    return render_template("admin_manage_students.html")

@admin_bp.route("/manage-exams")
@login_required
def manage_exams():
    return render_template("admin_manage_exams.html")

@admin_bp.route("/results")
@login_required
def results():
    return render_template("admin_results.html")
