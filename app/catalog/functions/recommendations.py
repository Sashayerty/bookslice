from sqlalchemy.orm import Session

from app.models.books import Books
from app.models.db_session import create_session, global_init


def session_create() -> Session:
    global_init("app/app.db")
    db_session = create_session()
    return db_session


def recommendations(
    db_session: Session = session_create(),
    authors: list[int] = None,
    genres: list[int] = None,
    read_books: list[int] = [],
) -> set[int] | None:
    """Функция для рекомендаций пользователю.

    Args:
        db_session (Session): Сессия бд. Defaults to None.
        authors (list[int], optional): Список авторов, книги которых читал пользователь.
        genres (list[int], optional): Список жанров, которые читал пользователь. Defaults to None.
        read_books (list[int], optional): Список книг, которые читал пользователь. Defaults to [].

    Returns:
        ids_of_books (set[int] | None): Множество идентификаторов книг, которые рекомендованы пользователю.
    """
    ids_of_books = set()
    books = db_session.query(Books)

    if authors and genres:  # Если есть авторы и жанры
        for author in authors:
            for genre in genres:
                for i in list(
                    books.filter_by(
                        author=author,
                        genre=genre,
                    ).all()
                ):
                    if i.id not in read_books:
                        ids_of_books.add(i.id)
    if authors:  # Если есть авторы
        for author in authors:
            for i in list(
                books.filter_by(
                    author=author,
                ).all()
            ):
                if i.id not in read_books:
                    ids_of_books.add(i.id)
    if genres:  # Если есть жанры
        for genre in genres:
            for i in list(
                books.filter_by(
                    genre=genre,
                ).all()
            ):
                if i.id not in read_books:
                    ids_of_books.add(i.id)
    elif not (authors and genres):  # Если нет авторов и жанров
        return None
    return ids_of_books if ids_of_books else None
