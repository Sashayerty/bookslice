from .base_view import BaseView


class SummarizedBooksOfUserView(BaseView):
    column_list = ("id", "user_id", "book_id", "text")
    column_filters = ("user_id",)
    column_labels = {
        "id": "ID",
        "user_id": "ID юзера",
        "book_id": "ID книги",
        "text": "Текст",
    }
    column_searchable_list = (
        "user_id",
        "book_id",
    )

    def _shorten_text(view, context, model, name):
        text = getattr(model, name)
        return text[:200] + "..." if len(text) > 200 else text

    column_formatters = {"text": _shorten_text}
