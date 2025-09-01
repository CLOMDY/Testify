from extensions import db

class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)   # FK to student (User)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)   # FK to Exam

    # ✅ New field for approval status
    is_approved = db.Column(db.Boolean, default=False)

    # ✅ Relationships
    user = db.relationship("User", back_populates="enrollments")
    exam = db.relationship("Exam", back_populates="enrollments")
