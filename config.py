import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey123")

    # Use PostgreSQL in production (Render/Heroku/etc.)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://username:password@host:5432/databasename"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
