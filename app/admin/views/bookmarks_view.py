from .base_view import BaseView


class BookMarksView(BaseView):
    column_list = ("id", "user_id", "book_id", "page")
    column_filters = (
        "user_id",
        "book_id",
    )
    column_labels = {
        "id": "ID",
        "user_id": "ID юзера",
        "book_id": "ID книги",
        "page": "Страница",
    }
    column_searchable_list = ("user_id",)
