from flask import Flask, render_template
import models
import models.db_session

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return "This is my profile"


@app.route("/register")
def register():
    return "Register to our service"


@app.route("/login")
def login():
    return "Login to your account"


@app.route("/logout")
def logout():
    return "Logout from your account"


@app.route("/catalog")
def catalog():
    return "This is the catalog of books"


@app.route("/catalog/<int:book_id>")
def book_in_catalog(book_id: int):
    return f"This is the book with id {book_id}"


@app.route("/read/<int:book_id>")
def read_book_in_catalog(book_id: int):
    return f"You can read this book with id {book_id}"


def main():
    app.run(debug=True)


if __name__ == "__main__":
    models.db_session.global_init("db/app.db")
    main()
