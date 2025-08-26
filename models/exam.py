from extensions import db


class Exam(db.Model):
    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False, default=30)  # in minutes

    questions = db.relationship("Question", backref="exam", lazy=True)
    results = db.relationship("Result", backref="exam", lazy=True)
