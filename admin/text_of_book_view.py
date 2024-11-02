# from wtforms.ext.sqlalchemy.fields import QuerySelectField

# from models.books import Books

from .base_view import BaseView


class TextOfBook(BaseView):
    def _shorten_text(view, context, model, name):
        text = getattr(model, name)
        return text[:200] + "..." if len(text) > 200 else text

    column_formatters = {"text": _shorten_text}
    column_list = ("book_id", "text")
    column_filters = ("book_id",)
    column_labels = {"book_id": "ID", "text": "Текст"}
    column_searchable_list = ("book_id",)
    # form_ajax_refs = {
    #     "book_id": {
    #         "fields": [
    #             "title"
    #         ],  # Поле title из модели Books будет использоваться для поиска
    #         "page_size": 10,  # Количество записей в автоподстановке
    #     }
    # }

    # # Переопределяем форму, чтобы book_id отображался как выпадающий список с книгами
    # form_overrides = {
    #     "book_id": QuerySelectField  # Поле будет поддерживать выбор из связанных записей
    # }

    # # Настраиваем форму, чтобы book_id ссылался на модель Books
    # form_args = {
    #     "book_id": {
    #         "query_factory": lambda: Books.query,  # Фабрика запросов для автоподстановки
    #         "get_pk": lambda book: book.id,  # Используем id книги как primary key
    #         "get_label": lambda book: book.title,  # Отображаем название книги
    #     }
    # }
