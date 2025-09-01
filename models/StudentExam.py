# student_exam.py
from extensions import db

class StudentExam(db.Model):
    __tablename__ = "student_exams"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)  # approval status

    student = db.relationship("User", backref="enrollments")
    exam = db.relationship("Exam", backref="enrollments")
