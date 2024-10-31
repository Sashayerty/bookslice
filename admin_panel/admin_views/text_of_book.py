from flask_admin.contrib.sqla import ModelView


class TextOfBook(ModelView):
    def _shorten_text(view, context, model, name):
        text = getattr(model, name)
        return text[:200] + "..." if len(text) > 200 else text

    column_formatters = {"text": _shorten_text}
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ("book_id", "text")
    column_filters = ("book_id",)
    column_labels = {"book_id": "ID", "text": "Текст"}
