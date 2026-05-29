import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "nutrition_app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-super-secret")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    REPORT_FOLDER = os.path.join(BASE_DIR, "static", "reports")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024