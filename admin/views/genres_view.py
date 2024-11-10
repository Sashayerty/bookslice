from .base_view import BaseView


class GenresView(BaseView):
    column_list = ("id", "name", "en_name")
    column_filters = ("name",)
    column_labels = {
        "id": "ID",
        "name": "Название",
        "en_name": "Название на латинице",
    }
    column_searchable_list = ("name",)
    column_editable_list = ("name", "en_name")
