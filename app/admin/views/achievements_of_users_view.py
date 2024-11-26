from .base_view import BaseView


class AchievementsOfUsersView(BaseView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = (
        "id",
        "user_id",
        "achievement_id",
    )
    column_filters = (
        "user_id",
        "achievement_id",
    )
    column_labels = {
        "id": "ID",
        "user_id": "ID юзера",
        "achievement_id": "ID ачивки",
    }
    column_editable_list = (
        "user_id",
        "achievement_id",
    )
    column_searchable_list = ("user_id",)
