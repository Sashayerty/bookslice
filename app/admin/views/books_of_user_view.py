from .base_view import BaseView


class BooksOfUserView(BaseView):
    column_list = (
        "id",
        "user_id",
        "book_id",
        "status",
    )
    column_filters = (
        "user_id",
        "book_id",
    )
    column_labels = {
        "id": "ID",
        "user_id": "ID юзера",
        "book_id": "ID книги",
        "status": "Статус",
    }
    column_editable_list = (
        "user_id",
        "book_id",
        "status",
    )
    column_searchable_list = ("user_id", "book_id")
