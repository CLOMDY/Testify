from extensions import db

class Exam(db.Model):
    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=30)  # in minutes

    # Delete cascade
    questions = db.relationship(
        "Question", backref="exam", cascade="all, delete-orphan", lazy=True
    )
    results = db.relationship(
        "Result", backref="exam", cascade="all, delete-orphan", lazy=True
    )

    # 🔥 Use back_populates instead of duplicate backref
    enrollments = db.relationship(
        "Enrollment",
        back_populates="exam",
        lazy=True,
        cascade="all, delete-orphan"
    )
