import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Основные настройки проекта `app.py`."""

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "your-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "False") == "True"
    DATABASE_URI = os.getenv("DATABASE_URI", "db/app.db")
    ADMIN_TEMPLATE_MODE = "bootstrap3"  # bootstrap2, bootstrap3, bootstrap4
    # FLASK_ADMIN_SWATCH = ""  # Это тема админки. Все темы тут: https://bootswatch.com/


config = Config()
