from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

# Blueprint for student routes
student_bp = Blueprint("student", __name__, url_prefix="/student")

# Student Dashboard
@student_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "student":
        return "Unauthorized", 403
    return render_template("student_dashboard.html")

# Available Exams
@student_bp.route("/exams")
@login_required
def available_exams():
    if current_user.role != "student":
        return "Unauthorized", 403
    return render_template("student_exams.html")  # new file

# Results
@student_bp.route("/results")
@login_required
def results():
    if current_user.role != "student":
        return "Unauthorized", 403
    return render_template("student_results.html")  # new file
