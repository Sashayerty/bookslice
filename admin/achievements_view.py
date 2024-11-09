from .base_view import BaseView


class AchievementsView(BaseView):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = (
        "id",
        "title",
        "description",
        "type",
        "condition",
        "reward",
    )
    column_filters = ("title", "type", "reward")
    column_labels = {
        "id": "ID",
        "title": "Название",
        "description": "Описание",
        "type": "Тип",
        "condition": "Требование",
        "reward": "Награда",
    }
    column_editable_list = (
        "title",
        "description",
        "type",
        "condition",
        "reward",
    )
    column_searchable_list = (
        "title",
        "description",
        "type",
        "condition",
    )
