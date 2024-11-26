from .base_view import BaseView


class NotificationsView(BaseView):
    column_list = ("type", "user_id", "data")
    column_filters = ("user_id",)
    column_labels = {
        "type": "Тип",
        "user_id": "ID юзера",
        "data": "Данные",
    }
    column_searchable_list = (
        "type",
        "user_id",
    )
    can_edit = False
