from flask_admin.contrib.sqla import ModelView


class TextOfBook(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ("book_id", "text")
