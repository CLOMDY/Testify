import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey123")

    # PostgreSQL local connection
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:admin123@localhost/exam_portal"


    SQLALCHEMY_TRACK_MODIFICATIONS = False
