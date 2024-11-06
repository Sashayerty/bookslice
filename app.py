import os.path as op
from datetime import datetime

from flask import Flask, redirect, render_template, session, url_for
from flask_admin import Admin, AdminIndexView
from flask_babel import Babel
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from admin import (
    AuthorsView,
    BooksView,
    GeneresView,
    StaticFilesView,
    TextOfBookView,
    UsersView,
)
from admin.localization.localization import get_locale
from config import config
from functions import AI, summarize_text
from models import Authors, Books, Generes, TextOfBook, User, db_session
from static.forms import (
    ChatForm,
    LoginForm,
    RegisterForm,
    SummByIdForm,
    SummForm,
)

# Создание констант для работы проекта

app = Flask(__name__)
app.config.from_object(config)

adminka = Admin(
    app,
    name="BookSlice Admin",
    index_view=AdminIndexView(name="BookSlice Admin", url="/admin"),
    template_mode=app.config["ADMIN_TEMPLATE_MODE"],
)

ai = AI()

db_session.global_init(app.config["DATABASE_URI"])
db_sess = db_session.create_session()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "unauthorized"

path = op.join(op.dirname(__file__), "static")

babel = Babel(app, locale_selector=get_locale)

# Добавление моделей в админку

adminka.add_views(
    BooksView(
        Books,
        db_sess,
        name="Книги",
        category="Модели",
    ),
    AuthorsView(
        Authors,
        db_sess,
        name="Авторы",
        category="Модели",
    ),
    GeneresView(
        Generes,
        db_sess,
        name="Жанры",
        category="Модели",
    ),
    TextOfBookView(
        TextOfBook,
        db_sess,
        name="Тексты книг",
        category="Модели",
    ),
    UsersView(
        User,
        db_sess,
        name="Пользователи",
        category="Модели",
    ),
)
adminka.add_view(
    StaticFilesView(
        path,
        "/static/",
        name="Статические Файлы",
    )
)

# Маршруты


@login_manager.user_loader
def load_user(user_id):
    """Загрузка юзера"""
    return db_sess.query(User).get(user_id)


@app.route("/unauthorized")
def unauthorized():
    """Страница для неавторизованных пользователей"""
    return render_template("unauth.html", title="Войдите в аккаунт"), 401


@app.route("/not-found")
def not_found():
    """Страница для ненайденных страниц"""
    return render_template("404.html", title="404 Not Found"), 404


# Обработчик ошибки 401
@app.errorhandler(404)
def custom_404(error):
    """Кастомный обработчик 404 ошибки"""
    return redirect(url_for("not_found"))


# Обработчик ошибки 401
@app.errorhandler(401)
def custom_401(error):
    """Кастомный обработчик 401 ошибки"""
    return redirect(url_for("unauthorized"))


@app.route("/")
def index():
    """Главная страница"""
    return render_template(
        "index.html",
        title="Главная",
        user_is_auth=current_user.is_authenticated,
        admin=current_user.admin if current_user.is_authenticated else False,
    )


@app.route("/profile")
@login_required
def profile():
    """Страница профиля"""
    db_sess = db_session.create_session()
    name = db_sess.query(User).get(current_user.id).name
    email = db_sess.query(User).get(current_user.id).email
    speed_of_reading = (
        db_sess.query(User).get(current_user.id).speed_of_reading
    )
    return render_template(
        "profile.html",
        title="Профиль",
        name=name,
        email=email,
        id=current_user.id,
        user_is_auth=current_user.is_authenticated,
        speed_of_reading=speed_of_reading,
        admin=current_user.admin if current_user.is_authenticated else False,
    )


@app.route("/summarize", methods=["POST", "GET"])
@login_required
def summarize():
    """Страница сжатия"""
    form = SummForm()
    if form.is_submitted():
        if form.type_of_sum.data == "Сильное сжатие":
            text = summarize_text(form.text.data[:1000000], "strong")
            return render_template(
                "read_book.html",
                title="Сжатая книга",
                text_of_book=text,
                summ_text="Сжатый текст",
                user_is_auth=current_user.is_authenticated,
                admin=(
                    current_user.admin
                    if current_user.is_authenticated
                    else False
                ),
            )
        else:
            text = summarize_text(form.text.data[:1000000], "weak")
            return render_template(
                "read_book.html",
                title="Сжатая книга",
                text_of_book=text,
                summ_text="Сжатый текст",
                user_is_auth=current_user.is_authenticated,
                admin=(
                    current_user.admin
                    if current_user.is_authenticated
                    else False
                ),
            )
    return render_template(
        "summarize.html",
        user_is_auth=current_user.is_authenticated,
        admin=current_user.admin if current_user.is_authenticated else False,
        title="Сжать книгу",
        form=form,
    )


@app.route("/summarize/<int:book_id>", methods=["POST", "GET"])
@login_required
def summarize_by_id(book_id):
    """Страница сжатия конкретной книги по id"""
    form = SummByIdForm()
    book = db_sess.query(Books).get(book_id)
    if book:
        if form.is_submitted():
            text_of_book = (
                db_sess.query(TextOfBook)
                .filter_by(book_id=book.id)
                .first()
                .text
            )
            if form.type_of_sum.data == "Сильное сжатие":
                text = summarize_text(text_of_book, "strong")
                return render_template(
                    "read_book.html",
                    title=f"Сжатое произведение {book.title}",
                    text_of_book=text,
                    summ_text=f"Сжатое произведение {book.title}",
                    user_is_auth=current_user.is_authenticated,
                    admin=(
                        current_user.admin
                        if current_user.is_authenticated
                        else False
                    ),
                )
            else:
                text = summarize_text(text_of_book, "weak")
                return render_template(
                    "read_book.html",
                    title=f"Сжатое произведение {book.title}",
                    text_of_book=text,
                    summ_text=f"Сжатое произведение {book.title}",
                    user_is_auth=current_user.is_authenticated,
                    admin=(
                        current_user.admin
                        if current_user.is_authenticated
                        else False
                    ),
                )
        return render_template(
            "summarize.html",
            user_is_auth=current_user.is_authenticated,
            admin=(
                current_user.admin if current_user.is_authenticated else False
            ),
            title=f"Сжать {book.title}",
            form=form,
            book=book,
        )
    else:
        return (
            render_template(
                "404.html",
                title="404 Not Found",
            ),
            404,
        )


@app.route("/check-speed-of-reading")
@login_required
def check_speed_of_reading():
    """Страница проверки скорости чтения"""
    return render_template(
        "check_speed_of_reading.html",
        title="Проверить скорость чтения",
        user_is_auth=current_user.is_authenticated,
        admin=current_user.admin if current_user.is_authenticated else False,
    )


@app.route("/test/<int:book_id>")
@login_required
def test_by_book(book_id: int):
    """Страница теста по книге"""
    book = db_sess.query(Books).get(book_id)
    if book:
        return render_template(
            "test_by_book.html",
            title="Тест",
            user_is_auth=current_user.is_authenticated,
            admin=(
                current_user.admin if current_user.is_authenticated else False
            ),
            book=book,
        )
    else:
        return (
            render_template(
                "404.html",
                title="404 Not Found",
            ),
            404,
        )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Страница регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Пароли не совпадают",
            )
        if len(form.password.data) < 8:
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Длина пароля должна быть не менее 8 символов",
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template("register.html", title="Регистрация", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    """Страница входа"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = (
            db_sess.query(User).filter(User.email == form.email.data).first()
        )
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html", message="Неправильный логин или пароль", form=form
        )
    return render_template("login.html", title="Вход", form=form)


@app.route("/admin-login", methods=["POST", "GET"])
def admin_login():
    """Страница входа в админку"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = (
            db_sess.query(User).filter(User.email == form.email.data).first()
        )
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/admin")
        elif user and not user.admin:
            return render_template(
                "admin/admin_login.html",
                message="У Вас нет доступа к админ-панели!",
                form=form,
            )
        return render_template(
            "admin/admin_login.html",
            message="Неправильный логин или пароль",
            form=form,
        )
    return render_template(
        "admin/admin_login.html", title="BookSlice Admin", form=form
    )


@app.route("/logout")
@login_required
def logout():
    """Страница выхода"""
    logout_user()
    return redirect("/")


@app.route("/ask", methods=["GET", "POST"])
@login_required
def ask():
    """Страница для общения с ИИ"""
    form = ChatForm()
    if form.validate_on_submit():
        messages = ai.message(form.message.data)
        messages = ai.get_messages()
        return render_template(
            "ask.html",
            title="Спросить ИИ",
            form=form,
            user_is_auth=current_user.is_authenticated,
            admin=(
                current_user.admin if current_user.is_authenticated else False
            ),
            messages=messages,
        )
    messages = ai.get_messages()
    return render_template(
        "ask.html",
        title="Спросить ИИ",
        form=form,
        user_is_auth=current_user.is_authenticated,
        admin=current_user.admin if current_user.is_authenticated else False,
        messages=messages,
    )


@app.route("/catalog")
@login_required
def catalog():
    """Страница каталога"""
    db_sess = db_session.create_session()
    books = db_sess.query(Books).all()
    generes = db_sess.query(Generes).all()
    return render_template(
        "catalog.html",
        title="Каталог",
        user_is_auth=current_user.is_authenticated,
        admin=current_user.admin if current_user.is_authenticated else False,
        books=books,
        generes=generes,
    )


@app.route("/catalog/<int:book_id>")
@login_required
def book_in_catalog(book_id: int):
    """Страница книги"""
    db_sess = db_session.create_session()
    book = db_sess.query(Books).get(book_id)
    if book:
        author = db_sess.query(Authors).get(book.author)
        genere = db_sess.query(Generes).get(book.genere)
        return render_template(
            "about_book.html",
            title=book.title,
            user_is_auth=current_user.is_authenticated,
            admin=(
                current_user.admin if current_user.is_authenticated else False
            ),
            book=book,
            author=author,
            genere=genere,
        )
    else:
        return (
            render_template(
                "404.html",
                title="404 Not Found",
            ),
            404,
        )


@app.route("/catalog/<string:genere_name>")
@login_required
def sort_catalog_by_genere(genere_name: str):
    """Страница каталога, отсортированного по жанру"""
    genere = db_sess.query(Generes).filter_by(en_name=genere_name).first()
    if genere:
        generes = db_sess.query(Generes).all()
        books = db_sess.query(Books).filter_by(genere=genere.id).all()
        return render_template(
            "catalog.html",
            title="Каталог",
            books=books,
            user_is_auth=current_user.is_authenticated,
            admin=(
                current_user.admin if current_user.is_authenticated else False
            ),
            generes=generes,
        )
    else:
        return (
            render_template(
                "404.html",
                title="404 Not Found",
            ),
            404,
        )


@app.route("/read/<int:book_id>")
@login_required
def read_book_in_catalog(book_id: int):
    """Страница чтения книги"""
    db_sess = db_session.create_session()
    book = db_sess.query(Books).get(book_id)
    if book:
        text_of_book = db_sess.query(TextOfBook).get(book_id).text
        author = db_sess.query(Authors).get(book.author).name
        return render_template(
            "read_book.html",
            title=book.title,
            user_is_auth=current_user.is_authenticated,
            admin=(
                current_user.admin if current_user.is_authenticated else False
            ),
            text_of_book=text_of_book,
            book=book,
            author=author,
        )
    else:
        return (
            render_template(
                "404.html",
                title="404 Not Found",
            ),
            404,
        )


@app.route("/start-test", methods=["POST", "GET"])
@login_required
def start_test():
    """Старт теста скорости чтения"""
    session["start_time"] = datetime.now().isoformat()
    return "", 204


@app.route("/end-test", methods=["POST", "GET"])
@login_required
def end_test():
    """Конец теста скорости чтения"""
    start_time_str = session.get("start_time")
    if start_time_str is None:
        return redirect("/not-found")

    start_time = datetime.fromisoformat(start_time_str)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60

    word_count = 188

    reading_speed = word_count / duration

    db_sess.query(User).get(current_user.id).speed_of_reading = int(
        reading_speed
    )
    db_sess.commit()
    session["start_time"] = None
    return redirect("/profile")


def main():
    """Запуск проекта"""
    app.run(debug=app.config["DEBUG"])


if __name__ == "__main__":
    main()
