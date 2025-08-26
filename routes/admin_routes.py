from flask import Blueprint, render_template
from flask_login import login_required, current_user

# Blueprint for admin routes
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "admin":
        return "Unauthorized", 403
    return render_template("admin/dashboard.html")
