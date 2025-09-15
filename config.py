import os

class Config:
    # Secret key → must come from environment in production
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey123")

    # Database URI → must be provided via environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional engine tuning for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": int(os.environ.get("DB_POOL_SIZE", 10)),
        "max_overflow": int(os.environ.get("DB_MAX_OVERFLOW", 20)),
        "pool_timeout": int(os.environ.get("DB_POOL_TIMEOUT", 30)),
        "pool_pre_ping": True,
    }
