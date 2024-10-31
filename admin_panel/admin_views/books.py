from flask_admin.contrib.sqla import ModelView


class Books(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ("id", "title", "author", "writed_in", "original", "genere")
    column_filters = ("title", "genere", "original")
    column_labels = {
        "id": "ID",
        "title": "Название книги",
        "author": "Автор",
        "writed_in": "Год издания",
        "original": "Оригинальность",
        "genere": "Жанр",
    }
