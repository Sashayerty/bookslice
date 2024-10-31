from .base_view import BaseView


class Books(BaseView):
    column_list = ("id", "title", "author", "writed_in", "original", "genere")
    column_filters = ("title", "genere", "original")
    column_labels = {
        "id": "ID",
        "description": "Описание",
        "count_of_words": "Количество слов",
        "title": "Название книги",
        "author": "Автор",
        "writed_in": "Год издания",
        "original": "Оригинальность",
        "genere": "Жанр",
    }
    column_editable_list = (
        "title",
        "author",
        "writed_in",
        "genere",
        "original",
    )
    column_searchable_list = ("title", "author")
