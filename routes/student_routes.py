from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models.exam import Exam
from models.result import Result  # optional, if you want to check attempted exams

from models.exam import Exam
from models.question import Question
from models.answer import Answer
from models.result import Result
from extensions import db
from flask import request, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from models.enrollment import Enrollment

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

    # Fetch all exams
    exams = Exam.query.filter_by(created_by=current_user.teacher_id).all()

    # Optionally, you can filter out exams already attempted by the student
    # attempted_exam_ids = [r.exam_id for r in Result.query.filter_by(user_id=current_user.id).all()]
    # exams = [exam for exam in exams if exam.id not in attempted_exam_ids]

    return render_template("student_exams.html", exams=exams)

@student_bp.route("/take-exam/<int:exam_id>", methods=["GET", "POST"])
@login_required
def take_exam(exam_id):
    if current_user.role != "student":
        return "Unauthorized", 403

    enrollment = Enrollment.query.filter_by(
    user_id=current_user.id,
    exam_id=exam_id,
    is_approved=True
    ).first()

    if not enrollment:
        flash("You are not approved to take this exam yet.", "danger")
        return redirect(url_for("student.available_exams"))
    
    exam = Exam.query.get_or_404(exam_id)

    if request.method == "POST":
        # 1️⃣ Create a Result for this student and exam
        result = Result(user_id=current_user.id, exam_id=exam.id, score=0)
        db.session.add(result)
        db.session.commit()  # commit to get result.id

        score = 0

        # 2️⃣ Loop through questions and save answers
        for q in exam.questions:
            selected_option = request.form.get(f"question_{q.id}")
            is_correct = selected_option == q.correct_option

            answer = Answer(
                result_id=result.id,
                question_id=q.id,
                selected_option=selected_option,
                is_correct=is_correct
            )
            db.session.add(answer)

            if is_correct:
                score += 1

        # 3️⃣ Update result score
        result.score = score
        db.session.commit()

        flash(f"Exam submitted! You scored {score} out of {len(exam.questions)}", "success")
        return redirect(url_for("student.results"))

    # GET request — render exam
    return render_template("take_exam.html", exam=exam)

# Student requests enrollment for an exam
@student_bp.route("/request-enrollment/<int:exam_id>", methods=["POST"])
@login_required
def request_enrollment(exam_id):
    if current_user.role != "student":
        return "Unauthorized", 403

    # check if already requested
    existing = Enrollment.query.filter_by(user_id=current_user.id, exam_id=exam_id).first()
    if existing:
        flash("You have already requested/enrolled for this exam.", "info")
        return redirect(url_for("student.available_exams"))

    enrollment = Enrollment(user_id=current_user.id, exam_id=exam_id, status="pending")
    db.session.add(enrollment)
    db.session.commit()

    flash("Enrollment request sent. Waiting for approval.", "success")
    return redirect(url_for("student.available_exams"))


@student_bp.route("/enroll_exam/<int:exam_id>", methods=["POST"])
@login_required
def enroll_exam(exam_id):
    if current_user.role != "student":
        flash("Only students can enroll in exams.", "danger")
        return redirect(url_for("auth.login"))

    enrollment = Enrollment(user_id=current_user.id, exam_id=exam_id, is_approved=False)
    db.session.add(enrollment)
    db.session.commit()

    flash("Enrollment request sent. Wait for approval.", "success")
    # Fix endpoint here:
    return redirect(url_for("student.available_exams"))


@student_bp.route("/submit-exam/<int:exam_id>", methods=["POST"])
@login_required
def submit_exam(exam_id):
    if current_user.role != "student":
        return "Unauthorized", 403

    exam = Exam.query.get_or_404(exam_id)

    # Loop through questions and capture answers
    for q in exam.questions:
        answer = request.form.get(f"answer_{q.id}")
        if answer:
            # Save answer logic here (to your Answer or Result table)
            pass

    flash("Exam submitted successfully!", "success")
    return redirect(url_for("student.dashboard"))


# Results
@student_bp.route("/results")
@login_required
def results():
    if current_user.role != "student":
        return "Unauthorized", 403

    # Fetch all results of the current student
    results = Result.query.filter_by(user_id=current_user.id).all()

    return render_template("student_results.html", results=results)
