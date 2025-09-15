import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "ef4fac15fb41bab4006170bf83b0226bde75921d53d31ac49d73d134e934f34f")

    # Primary DB URI — set DATABASE_URL in environment
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://testify_e8w5_user:VoROx2PEvRkSxkDg6KEKiu1EjeYhetxw@dpg-d3404lripnbc73ec071g-a/testify_e8w5"   # fallback for local dev if you want
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional engine tuning for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": int(os.environ.get("DB_POOL_SIZE", 10)),
        "max_overflow": int(os.environ.get("DB_MAX_OVERFLOW", 20)),
        "pool_timeout": int(os.environ.get("DB_POOL_TIMEOUT", 30)),
        "pool_pre_ping": True
    }
