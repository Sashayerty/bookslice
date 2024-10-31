from .base_view import BaseView


class UsersView(BaseView):
    can_create = False
    column_list = ("id", "name", "email", "speed_of_reading", "admin")
    column_filters = ("name", "email", "admin")
    column_labels = {
        "id": "ID",
        "name": "Имя",
        "email": "Почта",
        "speed_of_reading": "Скорость чтения",
        "admin": "Администратор",
        "created_date": "Дата создания",
    }
    column_editable_list = (
        "name",
        "email",
        "speed_of_reading",
        "admin",
    )
    column_searchable_list = ("name", "email")
