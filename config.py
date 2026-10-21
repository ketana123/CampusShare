import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration loaded from environment variables (.env)."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # --- Database ---------------------------------------------------
    # Preferred: set DATABASE_URL directly, e.g.
    #   mysql+pymysql://user:password@localhost/campusshare
    # If DATABASE_URL is not set, a local SQLite file is used instead so the
    # project can be run immediately without installing MySQL.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'instance', 'campusshare.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- College restriction ----------------------------------------
    COLLEGE_EMAIL_DOMAIN = os.environ.get("COLLEGE_EMAIL_DOMAIN", "mycollege.edu")

    # --- Uploads ------------------------------------------------------
    UPLOAD_FOLDER = os.path.join(basedir, "uploads", "items")
    ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB

    # --- Sessions / security -----------------------------------------
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    WTF_CSRF_ENABLED = True

    ITEMS_PER_PAGE = 9


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
