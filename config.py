import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey123")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost/exam_portal"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False