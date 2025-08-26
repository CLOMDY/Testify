from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import Exam, Question   # make sure you have these models

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "admin":
        flash("Unauthorized access", "danger")
        return redirect(url_for("auth.login"))
    return render_template("admin_dashboard.html")


@admin_bp.route("/manage-students")
@login_required
def manage_students():
    if current_user.role != "admin":
        flash("Unauthorized access", "danger")
        return redirect(url_for("auth.login"))
    return render_template("admin_manage_students.html")


# ✅ Manage exams page (GET: show form, POST: handle form submission)
@admin_bp.route("/manage-exams", methods=["GET", "POST"])
@login_required
def manage_exams():
    if current_user.role != "admin":
        flash("Unauthorized access", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        exam_title = request.form.get("exam_title")
        if not exam_title:
            flash("Exam title is required", "danger")
            return redirect(url_for("admin.manage_exams"))

        # Create new exam
        new_exam = Exam(title=exam_title)
        db.session.add(new_exam)
        db.session.commit()

        # Add questions
        for i in range(1, 31):
            q_text = request.form.get(f"question_{i}")
            optA = request.form.get(f"optionA_{i}")
            optB = request.form.get(f"optionB_{i}")
            optC = request.form.get(f"optionC_{i}")
            optD = request.form.get(f"optionD_{i}")
            correct = request.form.get(f"correct_{i}")

            if q_text and correct:
                question = Question(
                    exam_id=new_exam.id,
                    text=q_text,
                    optionA=optA,
                    optionB=optB,
                    optionC=optC,
                    optionD=optD,
                    correct_option=correct
                )
                db.session.add(question)

        db.session.commit()
        flash("Exam created successfully!", "success")
        return redirect(url_for("admin.manage_exams"))

    # ✅ GET request: show form + existing exams
    exams = Exam.query.all()
    return render_template("admin_manage_exams.html", exams=exams)


@admin_bp.route("/results")
@login_required
def results():
    if current_user.role != "admin":
        flash("Unauthorized access", "danger")
        return redirect(url_for("auth.login"))
    return render_template("admin_results.html")
