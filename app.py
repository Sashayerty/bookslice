from datetime import datetime
import os
import os.path as op

import dotenv
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

import admin
import admin.authors_view
import admin.books_view
import admin.generes_view
import admin.localozation.localization
import admin.static_files_view
import admin.text_of_book_view
import admin.users_view
import functions
import functions.AI
import functions.sum_alg
import models
import models.books
import models.db_session
import models.generes
import models.text_of_book
import models.user
import static.forms
import static.forms.chat
import static.forms.login_form
import static.forms.reg_form
import static.forms.summ_by_id_form
import static.forms.summ_form

app = Flask(__name__)
dotenv.load_dotenv(dotenv.find_dotenv())
adminka = Admin(
    app,
    name="BookSlice Admin",
    index_view=AdminIndexView(name="BookSlice Admin", url="/admin"),
    template_mode="bootstrap3",
)
ai = functions.AI.AI()
models.db_session.global_init("db/app.db")
db_sess = models.db_session.create_session()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "unauthorized"
path = op.join(op.dirname(__file__), "static")
babel = Babel(app, locale_selector=admin.localozation.localization.get_locale)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
# app.config["FLASK_ADMIN_SWATCH"] = "Cosmo"

adminka.add_views(
    admin.books_view.Books(models.books.Books, db_sess, name="Книги"),
    admin.authors_view.Authors(models.authors.Authors, db_sess, name="Авторы"),
    admin.generes_view.Generes(models.generes.Generes, db_sess, name="Жанры"),
    admin.text_of_book_view.TextOfBook(
        models.text_of_book.TextOfBook, db_sess, name="Тексты книг"
    ),
    admin.users_view.UsersView(models.user.User, db_sess, name="Пользователи"),
)
adminka.add_view(
    admin.static_files_view.StaticFiles(
        path, "/static/", name="Статические Файлы"
    )
)


@login_manager.user_loader
def load_user(user_id):
    db_sess = models.db_session.create_session()
    return db_sess.query(models.user.User).get(user_id)


@app.route("/unauthorized")
def unauthorized():
    return render_template("unauth.html", title="Войдите в аккаунт"), 401


@app.route("/not-found")
def not_found():
    return render_template("404.html", title="404 Not Found"), 404


# Обработчик ошибки 401
@app.errorhandler(404)
def custom_404(error):
    return redirect(url_for("not_found"))


# Обработчик ошибки 401
@app.errorhandler(401)
def custom_401(error):
    return redirect(url_for("unauthorized"))


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Главная",
        user_is_auth=current_user.is_authenticated,
        admin=current_user.admin if current_user.is_authenticated else False,
    )


@app.route("/profile")
@login_required
def profile():
    db_sess = models.db_session.create_session()
    name = db_sess.query(models.user.User).get(current_user.id).name
    email = db_sess.query(models.user.User).get(current_user.id).email
    speed_of_reading = (
        db_sess.query(models.user.User).get(current_user.id).speed_of_reading
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
    form = static.forms.summ_form.SummForm()
    if form.is_submitted():
        if form.type_of_sum.data == "Сильное сжатие":
            text = functions.sum_alg.summarize_text(
                form.text.data[:1000000], "strong"
            )
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
            text = functions.sum_alg.summarize_text(
                form.text.data[:1000000], "weak"
            )
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
    form = static.forms.summ_by_id_form.SummByIdForm()
    book = db_sess.query(models.books.Books).get(book_id)
    if book:
        if form.is_submitted():
            text_of_book = (
                db_sess.query(models.text_of_book.TextOfBook)
                .filter_by(book_id=book.id)
                .first()
                .text
            )
            if form.type_of_sum.data == "Сильное сжатие":
                text = functions.sum_alg.summarize_text(text_of_book, "strong")
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
                text = functions.sum_alg.summarize_text(text_of_book, "weak")
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

    return render_template(
        "summarize.html",
        user_is_auth=current_user.is_authenticated,
        admin=current_user.admin if current_user.is_authenticated else False,
        title="Сжать книгу",
        form=form,
    )


@app.route("/check-speed-of-reading")
@login_required
def check_speed_of_reading():
    return render_template(
        "check_speed_of_reading.html",
        title="Проверить скорость чтения",
        user_is_auth=current_user.is_authenticated,
        admin=current_user.admin if current_user.is_authenticated else False,
    )


@app.route("/test/<int:book_id>")
@login_required
def test_by_book(book_id: int):
    book = db_sess.query(models.books.Books).get(book_id)
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
    form = static.forms.reg_form.RegisterForm()
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
        db_sess = models.db_session.create_session()
        if (
            db_sess.query(models.user.User)
            .filter(models.user.User.email == form.email.data)
            .first()
        ):
            return render_template(
                "register.html",
                title="Регистрация",
                form=form,
                message="Такой пользователь уже есть",
            )
        user = models.user.User(
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
    form = static.forms.login_form.LoginForm()
    if form.validate_on_submit():
        db_sess = models.db_session.create_session()
        user = (
            db_sess.query(models.user.User)
            .filter(models.user.User.email == form.email.data)
            .first()
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
    form = static.forms.login_form.LoginForm()
    if form.validate_on_submit():
        db_sess = models.db_session.create_session()
        user = (
            db_sess.query(models.user.User)
            .filter(models.user.User.email == form.email.data)
            .first()
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
    logout_user()
    return redirect("/")


@app.route("/ask", methods=["GET", "POST"])
@login_required
def ask():
    form = static.forms.chat.ChatForm()
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
    db_sess = models.db_session.create_session()
    books = db_sess.query(models.books.Books).all()
    generes = db_sess.query(models.generes.Generes).all()
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
    db_sess = models.db_session.create_session()
    book = db_sess.query(models.books.Books).get(book_id)
    if book:
        author = db_sess.query(models.authors.Authors).get(book.author)
        genere = db_sess.query(models.generes.Generes).get(book.genere)
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
    genere = (
        db_sess.query(models.generes.Generes)
        .filter_by(en_name=genere_name)
        .first()
    )
    if genere:
        generes = db_sess.query(models.generes.Generes).all()
        books = (
            db_sess.query(models.books.Books).filter_by(genere=genere.id).all()
        )
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
    db_sess = models.db_session.create_session()
    book = db_sess.query(models.books.Books).get(book_id)
    if book:
        text_of_book = (
            db_sess.query(models.text_of_book.TextOfBook).get(book_id).text
        )
        author = db_sess.query(models.authors.Authors).get(book.author).name
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
    session["start_time"] = datetime.now().isoformat()
    return "", 204


@app.route("/end-test", methods=["POST", "GET"])
@login_required
def end_test():
    start_time_str = session.get('start_time')
    if start_time_str is None:
        return redirect("/not-found")

    start_time = datetime.fromisoformat(start_time_str)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60

    word_count = 188

    reading_speed = word_count / duration

    db_sess.query(models.user.User).get(current_user.id).speed_of_reading = (
        int(reading_speed)
    )
    db_sess.commit()
    session["start_time"] = None
    return redirect("/profile")


def main():
    app.run(debug=app.config["DEBUG"])


if __name__ == "__main__":
    main()
