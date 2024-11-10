# from wtforms.ext.sqlalchemy.fields import QuerySelectField

# from models.books import Books

from .base_view import BaseView


class TextOfBookView(BaseView):
    def _shorten_text(view, context, model, name):
        text = getattr(model, name)
        return text[:200] + "..." if len(text) > 200 else text

    column_formatters = {"text": _shorten_text}
    column_list = ("book_id", "text")
    column_filters = ("book_id",)
    column_labels = {"book_id": "ID", "text": "Текст"}
    column_searchable_list = ("book_id",)
