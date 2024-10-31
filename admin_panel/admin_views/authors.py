from flask_admin.contrib.sqla import ModelView


class Authors(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ("id", "name")
    column_filters = ("name",)
    column_labels = {"id": "ID", "name": "ФИО"}
