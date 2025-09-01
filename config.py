import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey123")

    # Use PostgreSQL in production (Render/Heroku/etc.)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://testify_bkx8_user:h3nBpRHuhZW1UkBZqGmHUvyNGyHtp0Kc@dpg-d2qkctqdbo4c73c86pk0-a/testify_bkx8"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
