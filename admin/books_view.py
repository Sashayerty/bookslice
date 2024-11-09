from .base_view import BaseView


class BooksView(BaseView):
    column_list = ("id", "title", "author", "wrote_in", "original", "genre")
    column_filters = ("title", "genre", "original")
    column_labels = {
        "id": "ID",
        "description": "Описание",
        "count_of_words": "Количество слов",
        "title": "Название книги",
        "author": "Автор",
        "wrote_in": "Год издания",
        "original": "Оригинальность",
        "genre": "Жанр",
    }
    column_editable_list = (
        "title",
        "author",
        "wrote_in",
        "genre",
        "original",
    )
    column_searchable_list = ("title", "author")
