class Config:
    """Основные настройки"""

    SECRET_KEY = "your-secret-key"
    DEBUG = True
    DATABASE_URI = "app/app.db"
    ADMIN_TEMPLATE_MODE = "bootstrap3"  # bootstrap2, bootstrap3, bootstrap4
    DEBUG_TB_INTERCEPT_REDIRECTS = (
        False  # Отключает переадресацию в flask-debugtoolbar
    )
    # FLASK_ADMIN_SWATCH = ""  # Это тема админки. Все темы тут: https://bootswatch.com/


config = Config()
