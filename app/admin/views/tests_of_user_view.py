from .base_view import BaseView


class TestsOfUserView(BaseView):
    column_list = ("id", "user_id", "summarized_book_id", "test")
    column_filters = ("user_id",)
    column_labels = {
        "id": "ID",
        "user_id": "ID юзера",
        "summarized_book_id": "ID книги",
        "test": "Тест",
    }
    column_searchable_list = (
        "user_id",
        "summarized_book_id",
    )

    def _shorten_test(view, context, model, name):
        text = getattr(model, name)
        return text[:200] + "..." if len(text) > 200 else text

    column_formatters = {"test": _shorten_test}
