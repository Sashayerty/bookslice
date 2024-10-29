import os

import dotenv
from flask import Flask, redirect, render_template
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

import forms
import forms.chat
import forms.login_form
import forms.reg_form
import models
import models.authors
import models.db_session
import models.text_of_book
import models.user

dotenv.load_dotenv(dotenv.find_dotenv())

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")


@login_manager.user_loader
def load_user(user_id):
    db_sess = models.db_session.create_session()
    return db_sess.query(models.user.User).get(user_id)


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Главная",
        user_is_auth=current_user.is_authenticated,
    )


@app.route("/profile")
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
    )


@app.route("/check-speed-of-reading")
def check_speed_of_reading():
    db_sess = models.db_session.create_session()
    db_sess.query(models.user.User).get(current_user.id).speed_of_reading = 120
    db_sess.commit()
    return redirect("/profile")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.reg_form.RegisterForm()
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
    form = forms.login_form.LoginForm()
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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/ask", methods=["GET", "POST"])
def ask():
    form = forms.chat.ChatForm()
    return render_template(
        "ask.html",
        title="Спросить ИИ",
        form=form,
        user_is_auth=current_user.is_authenticated,
    )


@app.route("/catalog")
def catalog():
    db_sess = models.db_session.create_session()
    books = db_sess.query(models.books.Books).all()
    return render_template(
        "catalog.html",
        title="Каталог",
        user_is_auth=current_user.is_authenticated,
        books=books,
    )


@app.route("/catalog/<int:book_id>")
def book_in_catalog(book_id: int):
    db_sess = models.db_session.create_session()
    book = db_sess.query(models.books.Books).get(book_id)
    author = db_sess.query(models.authors.Authors).get(book.author)
    return render_template(
        "about_book.html",
        title=book.title,
        user_is_auth=current_user.is_authenticated,
        book=book,
        author=author,
    )


@app.route("/read/<int:book_id>")
def read_book_in_catalog(book_id: int):
    db_sess = models.db_session.create_session()
    text_of_book = (
        db_sess.query(models.text_of_book.TextOfBook)
        .get(book_id)
        .text
    )
    return render_template(
        "read_book.html",
        title="Читать книгу",
        user_is_auth=current_user.is_authenticated,
        text_of_book=text_of_book,
    )


def main():
    app.run(debug=app.config["DEBUG"])


if __name__ == "__main__":
    models.db_session.global_init("db/app.db")
    main()
