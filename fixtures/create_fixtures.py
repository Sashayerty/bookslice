import json

import models
import models.authors
import models.books
import models.books_of_user
import models.db_session
import models.description_of_user
import models.generes
import models.text_of_book
import models.user


def create_fixtures():
    models.db_session.global_init("../db/app.db")
    db_sess = models.db_session.db_session.create_session()
    books = db_sess.query(models.books.Books).all()
    authors = db_sess.query(models.authors.Authors).all()
    books_of_user = db_sess.query(models.books_of_user.BooksOfUser).all()
    text_of_book = db_sess.query(models.text_of_book.TextOfBook).all()
    users = db_sess.query(models.user.User).all()
    generes = db_sess.query(models.generes.Generes).all()
    description_of_user = db_sess.query(
        models.description_of_user.DescriptionOfUser
    ).all()
    data = {
        "Books": [],
        "TextOfBook": [],
        "Authors": [],
        "BooksOfUser": [],
        "User": [],
        "Generes": [],
        "DescriptionOfUser": [],
    }
    for book in books:
        data["Books"].append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description,
                "author": book.author,
                "writed_in": book.writed_in,
                "count_of_words": book.count_of_words,
                "original": book.original,
                "genere": book.genere,
            }
        )
    for text in text_of_book:
        data["TextOfBook"].append(
            {"id": text.id, "book_id": text.book_id, "text": text.text}
        )

    for user in users:
        data["User"].append(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "hashed_password": user.hashed_password,
                "speed_of_reading": user.speed_of_reading,
                "created_date": user.created_date,
                "admin": user.admin,
            }
        )

    for author in authors:
        data["Authors"].append(
            {
                "id": author.id,
                "name": author.name,
            }
        )

    for book in books_of_user:
        data["BooksOfUser"].append(
            {
                "id": book.id,
                "user_id": book.user_id,
                "book_id": book.book_id,
                "status": book.status,
            }
        )

    for genere in generes:
        data["Generes"].append(
            {
                "id": genere.id,
                "name": genere.name,
            }
        )

    for d in description_of_user:
        data["DescriptionOfUser"].append(
            {
                "id": d.id,
                "user_id": d.user_id,
                "description": d.description,
            }
        )

    # Сохраняем данные в JSON-файл
    with open("fixtures.json", "w") as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

    print("Fixtures created successfully in fixtures.json.")


if __name__ == "__main__":
    create_fixtures()
