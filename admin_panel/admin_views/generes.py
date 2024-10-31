from .base_view import BaseView


class Generes(BaseView):
    column_list = ("id", "name")
    column_filters = ("name",)
    column_labels = {"id": "ID", "name": "Название"}
    column_searchable_list = ("name",)
