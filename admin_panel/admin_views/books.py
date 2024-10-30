from flask_admin.contrib.sqla import ModelView


class Books(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ("id", "title", "author", "writed_in", "original", "genere")
