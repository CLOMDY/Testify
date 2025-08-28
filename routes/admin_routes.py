from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models.exam import Exam
from models.question import Question
from models.enrollment import Enrollment
from models.user import User
from models.result import Result


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("admin_dashboard.html", user=current_user)

@admin_bp.route("/manage-students")
@login_required
def manage_students():
    if current_user.role != "admin":
        return redirect(url_for("auth.login"))

    exams = Exam.query.all()  # ✅ this will include updated enrollments
    return render_template("admin_manage_students.html", exams=exams)


# ✅ Manage exams with GET + POST
@admin_bp.route("/manage-exams", methods=["GET", "POST"])
@login_required
def manage_exams():
    if request.method == "POST":
        exam_title = request.form.get("exam_title")
        exam_duration = request.form.get("exam_duration")

        if not exam_title or not exam_duration:
            flash("Exam title and duration are required", "danger")
            return redirect(url_for("admin.manage_exams"))

        # Create new exam
        new_exam = Exam(title=exam_title, duration=int(exam_duration))
        db.session.add(new_exam)
        db.session.commit()

        # Add questions (optional: here just 1 question loop as example)
        for i in range(1, 6):  # you can extend this
            q_text = request.form.get(f"question_{i}")
            optA = request.form.get(f"optionA_{i}")
            optB = request.form.get(f"optionB_{i}")
            optC = request.form.get(f"optionC_{i}")
            optD = request.form.get(f"optionD_{i}")
            correct = request.form.get(f"correct_{i}")

            if q_text and correct:
                question = Question(
                    exam_id=new_exam.id,
                    question_text=q_text,
                    option_a=optA,
                    option_b=optB,
                    option_c=optC,
                    option_d=optD,
                    correct_option=correct
                )
                db.session.add(question)

        db.session.commit()
        flash("Exam created successfully!", "success")
        return redirect(url_for("admin.manage_exams"))

    # GET request: show form + existing exams
    exams = Exam.query.all()
    return render_template("admin_manage_exams.html", exams=exams)


@admin_bp.route("/edit-exam/<int:exam_id>", methods=["POST"])
@login_required
def edit_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)

    # Update exam title and duration
    new_title = request.form.get("exam_title")
    new_duration = request.form.get("exam_duration")
    if new_title:
        exam.title = new_title
    if new_duration:
        exam.duration = int(new_duration)

    # Update questions
    for q in exam.questions:
        q.question_text = request.form.get(f"question_{q.id}")
        q.option_a = request.form.get(f"option_a_{q.id}")
        q.option_b = request.form.get(f"option_b_{q.id}")
        q.option_c = request.form.get(f"option_c_{q.id}")
        q.option_d = request.form.get(f"option_d_{q.id}")
        q.correct_option = request.form.get(f"correct_{q.id}")

    db.session.commit()
    flash("Exam updated successfully!", "success")
    return redirect(url_for("admin.manage_exams"))


@admin_bp.route("/delete-exam/<int:exam_id>", methods=["POST"])
@login_required
def delete_exam(exam_id):
    if current_user.role != "admin":
        flash("Unauthorized access", "danger")
        return redirect(url_for("auth.login"))

    exam = Exam.query.get_or_404(exam_id)

    # Delete all associated questions first
    for q in exam.questions:
        db.session.delete(q)

    db.session.delete(exam)
    db.session.commit()
    flash("Exam deleted successfully!", "success")
    return redirect(url_for("admin.manage_exams"))


# Show enrollment requests
@admin_bp.route("/enrollments")
@login_required
def view_enrollments():
    if current_user.role != "admin":
        return "Unauthorized", 403

    enrollments = Enrollment.query.all()
    return render_template("admin_enrollments.html", enrollments=enrollments)


# Approve enrollment
@admin_bp.route("/approve-enrollment/<int:enrollment_id>", methods=["POST"])
@login_required
def approve_enrollment(enrollment_id):
    if current_user.role != "admin":
        return "Unauthorized", 403

    enrollment = Enrollment.query.get_or_404(enrollment_id)
    enrollment.is_approved = True   # ✅ update Boolean field
    db.session.commit()

    flash("Enrollment Accepted.", "success")
    return redirect(url_for("admin.manage_students"))

# Reject enrollment
@admin_bp.route("/reject-enrollment/<int:enrollment_id>", methods=["POST"])
@login_required
def reject_enrollment(enrollment_id):
    if current_user.role != "admin":
        return "Unauthorized", 403

    enrollment = Enrollment.query.get_or_404(enrollment_id)
    enrollment.status = "rejected"
    db.session.commit()
    
    flash("Enrollment rejected.", "warning")
    return redirect(url_for("admin.view_enrollments"))


@admin_bp.route("/approve_all/<int:exam_id>", methods=["POST"])
def approve_all(exam_id):
    enrollments = Enrollment.query.filter_by(exam_id=exam_id, is_approved=False).all()
    for e in enrollments:
        e.is_approved = True
    db.session.commit()
    flash("All students for this exam have been approved!", "success")
    return redirect(url_for("admin.manage_students"))

# Remove enrollment
@admin_bp.route("/remove-enrollment/<int:enrollment_id>", methods=["POST"])
@login_required
def remove_enrollment(enrollment_id):
    if current_user.role != "admin":
        return "Unauthorized", 403

    enrollment = Enrollment.query.get_or_404(enrollment_id)
    db.session.delete(enrollment)
    db.session.commit()

    flash("Enrollment removed successfully!", "success")
    return redirect(url_for("admin.manage_students"))


# Admin results page
@admin_bp.route("/results")
@login_required
def results():
    if current_user.role != "admin":
        return redirect(url_for("auth.login"))

    # Fetch all results with joined student and exam, in insertion order (FIFO)
    results = (
        db.session.query(Result, User, Exam)
        .join(User, Result.student_id == User.id)
        .join(Exam, Result.exam_id == Exam.id)
        .order_by(Result.id)  # <-- FIFO order
        .all()
    )

    # Group results by exam
    results_by_exam = {}
    for result, student, exam in results:
        if exam.id not in results_by_exam:
            results_by_exam[exam.id] = {
                "exam_title": exam.title,
                "results": []
            }
        results_by_exam[exam.id]["results"].append({
            "student_name": student.name,
            "score": result.score,
            "total_questions": len(exam.questions)
        })

    return render_template("admin_results.html", results_by_exam=results_by_exam)

# Leaderboard for a specific exam
# admin_routes.py
@admin_bp.route("/exam-leaderboard/<int:exam_id>")
@login_required
def exam_leaderboard(exam_id):
    exam = Exam.query.get_or_404(exam_id)

    # Fetch all results for this exam, ordered by score descending (so 1st is highest)
    results = Result.query.filter_by(exam_id=exam.id).order_by(Result.score.desc()).all()

    leaderboard = []
    for i, r in enumerate(results, start=1):
        student = User.query.get(r.student_id)
        leaderboard.append({
            "rank": int(i),  # ensure it's integer
            "student_name": student.name,
            "score": r.score,
            "total_questions": len(exam.questions)
        })

    return render_template("admin_leaderboard.html", exam=exam, leaderboard=leaderboard)
