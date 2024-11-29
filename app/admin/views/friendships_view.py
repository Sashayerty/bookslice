from .base_view import BaseView


class FriendshipsView(BaseView):
    column_list = ("id", "user_id", "friends_ids")
    column_filters = ("user_id",)
    column_labels = {
        "id": "ID",
        "user_id": "ID юзера",
        "friends_ids": "ID друзей",
    }
    column_searchable_list = ("user_id",)
