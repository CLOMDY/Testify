from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # required field
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "admin" or "student"

    # For admins
    teacher_key = db.Column(db.String(50), unique=True, nullable=True)

    # For students (link to their teacher/admin)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    teacher = db.relationship("User", remote_side=[id], backref="students")

    # Enrollments
    enrollments = db.relationship("Enrollment", back_populates="user", cascade="all, delete-orphan")

    # Exams created by the user (admins/teachers)
    exams = db.relationship("Exam", back_populates="creator", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
