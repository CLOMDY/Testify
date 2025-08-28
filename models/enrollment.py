from extensions import db

class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)

    # 🔥 Match back_populates
    student = db.relationship("User", back_populates="enrollments")
    exam = db.relationship("Exam", back_populates="enrollments")
