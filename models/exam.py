from extensions import db

class Exam(db.Model):
    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=30)

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relationships
    questions = db.relationship(
        "Question",
        backref="exam",
        cascade="all, delete-orphan",
        lazy=True
    )
    results = db.relationship(
        "Result",
        backref="exam",
        cascade="all, delete-orphan",
        lazy=True
    )
    enrollments = db.relationship(
        "Enrollment",
        back_populates="exam",
        cascade="all, delete-orphan",
        lazy=True
    )

    # ✅ Explicit back_populates
    creator = db.relationship("User", back_populates="exams")
