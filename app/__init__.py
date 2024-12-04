from flask import Flask, redirect, render_template, url_for
from flask_admin import Admin, AdminIndexView
from flask_babel import Babel
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, current_user

from app.admin.views.bookmarks_view import BookMarksView
from app.admin.views.friend_requests import FriendRequestsView
from app.admin.views.friendships_view import FriendshipsView
from app.config import config
from app.models.bookmarks import BookMarks
from app.models.friendships import Friendships

from .admin import (
    AchievementsOfUsersView,
    AchievementsView,
    AuthorsView,
    BooksOfUserView,
    BooksView,
    GenresView,
    NotificationsView,
    TextOfBookView,
    UsersView,
    get_locale,
)
from .models import (
    Achievements,
    AchievementsOfUsers,
    Authors,
    Books,
    BooksOfUser,
    Genres,
    Notifications,
    TextOfBook,
    Users,
    db_session,
)


def create_app():

    app = Flask(__name__)
    app.config.from_object(config)
    # if app.config["DEBUG"]:
    #     fdtb = DebugToolbarExtension(app=app)
    db_session.global_init(config.DATABASE_URI)
    db_ses = db_session.create_session()
    admin_panel = Admin(
        app,
        name="BookSlice Admin",
        index_view=AdminIndexView(
            name="BookSlice Admin",
            url="/admin",
        ),
        template_mode=app.config["ADMIN_TEMPLATE_MODE"],
    )
    admin_panel.add_views(
        BooksOfUserView(
            BooksOfUser,
            db_ses,
            name="Книги юзеров",
            category="Книги",
        ),
        BooksView(
            Books,
            db_ses,
            name="Книги",
            category="Книги",
        ),
        AuthorsView(
            Authors,
            db_ses,
            name="Авторы",
            category="Книги",
        ),
        GenresView(
            Genres,
            db_ses,
            name="Жанры",
            category="Книги",
        ),
        TextOfBookView(
            TextOfBook,
            db_ses,
            name="Тексты книг",
            category="Книги",
        ),
        UsersView(
            Users,
            db_ses,
            name="Пользователи",
            category="Модели",
        ),
        AchievementsView(
            Achievements,
            db_ses,
            name="Ачивки",
            category="Модели",
        ),
        AchievementsOfUsersView(
            AchievementsOfUsers,
            db_ses,
            name="Ачивки юзеров",
            category="Модели",
        ),
        FriendshipsView(
            Friendships,
            db_ses,
            name="Дружеские отношения",
            category="Друзья",
        ),
        NotificationsView(
            Notifications,
            db_ses,
            name="Уведомления",
            category="Модели",
        ),
        BookMarksView(
            BookMarks,
            db_ses,
            name="Закладки",
            category="Книги",
        ),
    )
    login_manager = LoginManager()
    login_manager.init_app(app)
    babel = Babel(
        app,
        locale_selector=get_locale,
    )

    def get_notifications() -> int:
        if current_user.is_authenticated:
            try:
                count_of_notifications = len(
                    db_ses.query(Notifications)
                    .filter_by(user_id=current_user.id)
                    .all()
                )
            except Exception:
                count_of_notifications = 0
        else:
            count_of_notifications = 0
        return count_of_notifications

    @login_manager.user_loader
    def load_user(user_id):
        """Загрузка юзера"""
        return db_ses.query(Users).get(user_id)

    @app.context_processor
    def inject_common_variables():
        notifications = get_notifications()
        return dict(notifications=notifications)

    @app.route("/unauthorized")
    def unauthorized():
        """Страница для неавторизованных пользователей"""
        return (
            render_template("./errors/unauth.html", title="Войдите в аккаунт"),
            401,
        )

    @app.route("/not-found")
    def not_found():
        """Страница для ненайденных страниц"""
        return (
            render_template("./errors/404.html", title="404 Not Found"),
            404,
        )

    # Обработчик ошибки 404
    @app.errorhandler(404)
    def custom_404(error):
        """Кастомный обработчик 404 ошибки"""
        return redirect(url_for("not_found"))

    # Обработчик ошибки 401
    @app.errorhandler(401)
    def custom_401(error):
        """Кастомный обработчик 401 ошибки"""
        return redirect(url_for("unauthorized"))

    from app.bookslice.routes import bookslice
    from app.catalog.routes import catalog
    from app.profile.routes import profile

    app.register_blueprint(
        bookslice,
    )
    app.register_blueprint(
        catalog,
        url_prefix="/catalog",
    )
    app.register_blueprint(
        profile,
        url_prefix="/profile",
    )

    return app
