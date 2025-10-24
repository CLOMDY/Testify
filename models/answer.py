from extensions import db

class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(
        db.Integer,
        db.ForeignKey("results.id", ondelete="CASCADE"),
        nullable=False
    )
    question_id = db.Column(
        db.Integer,
        db.ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )

    selected_option = db.Column(db.String(1), nullable=True)  # 'A', 'B', 'C', 'D'
    is_correct = db.Column(db.Boolean, nullable=False)
