import json

import requests
from dotenv import dotenv_values
from mistralai import Mistral
from sqlalchemy.orm import Session

from app.models.db_session import create_session, global_init


def session_create() -> Session:
    global_init("app/app.db")
    db_session = create_session()
    return db_session


def recommendations(
    db_session: Session = session_create(),
    user_id: int = None,
    read_books: list[int] = [],
) -> set[int]:
    """Функция для рекомендаций пользователю.

    Args:
        db_session (Session): Сессия бд. Defaults to None.
        authors (list[int], optional): Список авторов, книги которых читал пользователь.
        genres (list[int], optional): Список жанров, которые читал пользователь. Defaults to None.
        read_books (list[int], optional): Список книг, которые читал пользователь. Defaults to [].

    Returns:
        ids_of_books (set[int] | None): Множество идентификаторов книг, которые рекомендованы пользователю.
    """
    api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    response = requests.get(
        f"http://127.0.0.1:5000/get-user-data-for-ai?user_id={user_id}"
    ).text
    base = """
    Error:
    {
        "data": []
    }
    Good:
    {
        "data": [1, 2, 3, 4]
    }
    """
    prompt = f"""Ты - рекомендательная система. Твоя задача прислать список id книг,
    которые ты рекомендуешь к прочтению на основе УЖЕ прочитанных книг. Передавать нужно только те,
    которые есть в каталоге.
    Если тебе передается "error": "User id not found.", то возвращай []. Тебе данные с помощью json файла
    {response}. data_of_books_of_all_catalog -
    все книги в каталоге с названием и автором. read_data_of_user - книги,
    прочитанные юзером
    и общая информация по юзеру. Пример твоего ответа: {base}"""

    response = client.chat.complete(
        model="pixtral-large-latest",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format={
            "type": "json_object",
        },
    )
    return json.loads(response.choices[0].message.content)["data"]
