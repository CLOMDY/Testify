import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey123")

    # Use Render's DATABASE_URL if available, else fall back to local
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:admin123@localhost/exam_portal"
    )

    # Render gives DATABASE_URL as 'postgresql://', SQLAlchemy prefers 'postgresql+psycopg2://'
    if SQLALCHEMY_DATABASE_URI.startswith("postgresql://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgresql://", "postgresql+psycopg2://", 1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
