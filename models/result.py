from extensions import db


class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    percentile = db.Column(db.Float, nullable=True)

    answers = db.relationship("Answer", backref="result", lazy=True)
