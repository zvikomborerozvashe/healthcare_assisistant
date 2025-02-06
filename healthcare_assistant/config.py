import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = "sqlite:///healthcare.db"  # Using SQLite for now
    SQLALCHEMY_TRACK_MODIFICATIONS = False
