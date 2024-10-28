import os

import dotenv
from flask import Flask, redirect, render_template
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

import forms
import forms.login_form
import forms.reg_form
import models
import models.db_session
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
    return render_template(
        "profile.html",
        title="Профиль",
    )  # noqa


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


@app.route("/catalog")
def catalog():
    return render_template("catalog.html", title="Каталог")


@app.route("/catalog/<int:book_id>")
def book_in_catalog(book_id: int):
    return render_template("index.html", title="Информация о книге")


@app.route("/read/<int:book_id>/<int:page>")
def read_book_in_catalog(book_id: int, page: int):
    return render_template("index.html", title="Читать книгу")


def main():
    app.run(debug=app.config["DEBUG"])


if __name__ == "__main__":
    models.db_session.global_init("db/app.db")
    main()
