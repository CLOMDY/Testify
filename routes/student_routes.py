from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Blueprint for student routes
student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "student":
        return "Unauthorized", 403
    return render_template("student/dashboard.html")
