import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey123")
    # Use SQLite (creates a file exam_portal.db in project root)
    SQLALCHEMY_DATABASE_URI = "sqlite:///exam_portal.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
