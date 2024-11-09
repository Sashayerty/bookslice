from .base_view import BaseView


class UsersView(BaseView):
    can_create = False
    column_list = (
        "id",
        "name",
        "email",
        "speed_of_reading",
        "admin",
        "read_books",
        "read_pages",
        "summarized_books",
    )
    column_filters = ("name", "email", "admin")
    column_labels = {
        "id": "ID",
        "name": "Имя",
        "email": "Почта",
        "speed_of_reading": "Скорость чтения",
        "admin": "Админ",
        "created_date": "Дата создания",
        "read_books": "Прочитано книг",
        "read_pages": "Прочитано страниц",
        "summarized_books": "Ссумаризированно книг",
    }
    column_editable_list = (
        "name",
        "email",
        "speed_of_reading",
        "admin",
    )
    column_searchable_list = ("name", "email")
