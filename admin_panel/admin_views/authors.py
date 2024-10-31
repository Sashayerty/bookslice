from .base_view import BaseView


class Authors(BaseView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ("id", "name")
    column_filters = ("name",)
    column_labels = {"id": "ID", "name": "ФИО"}
    column_editable_list = ("name",)
    column_searchable_list = ("name",)
