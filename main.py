from flask import Flask, render_template
import models
import models.db_session

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Главная")


@app.route("/profile")
def profile():
    return render_template("index.html", title="Профиль")


@app.route("/register")
def register():
    return render_template("index.html", title="Регистрация")


@app.route("/login")
def login():
    return render_template("index.html", title="Войти")


@app.route("/logout")
def logout():
    return "Выход из аккаунта"


@app.route("/catalog")
def catalog():
    return render_template("index.html", title="Каталог")


@app.route("/catalog/<int:book_id>")
def book_in_catalog(book_id: int):
    return render_template("index.html", title="Информация о книге")


@app.route("/read/<int:book_id>/<int:page>")
def read_book_in_catalog(book_id: int, page: int):
    return render_template("index.html", title="Читать книгу")


def main():
    app.run(debug=True)


if __name__ == "__main__":
    models.db_session.global_init("db/app.db")
    main()
