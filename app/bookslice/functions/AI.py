import requests
from dotenv import dotenv_values
from markdown import markdown
from mistralai import Mistral

api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]


class AI:
    def __init__(self) -> None:
        self.client = Mistral(api_key=api_key)
        self.msgs = []
        self.prompt = {"messages": self.msgs}

    def message(self, mess, user_id):
        response = requests.get(
            f"http://127.0.0.1:5000/get-user-data-for-ai?user_id={user_id}"
        ).text
        print(response)
        self.msgs.append({"role": "user", "text": mess})
        self.prompt["messages"] = self.msgs
        self.chat_response = self.client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": f"""Ты - ИИ помощник для сайта-соцсети BookSlice, посвящённой чтению. Ты можешь
                    пользоваться информацией ТОЛЬКО из JSON файла
                    У нас доступно
                    отслеживание своего прогресса и добавление в друзья + отслеживание прогресса друзей Ты должен
                    поддерживать диалог, нейтрально относясь к острым темам. Ответы должны быть
                    ТОЛЬКО на русском. Не делай таблицы.
                    Тебе данные с помощью json файла {response}. data_of_books_of_all_catalog -
                    все книги в каталоге с названием и автором
                    которые следует советовать во время диалога (по ситуации). read_data_of_user - книги,
                    прочитанные юзером
                    и общая информация по юзеру. История сообщений с юзером:{self.msgs}""",
                },
            ],
        )
        response = markdown(self.chat_response.choices[0].message.content)
        self.prompt["messages"].append(
            {
                "role": "assistant",
                "text": response,
            }
        )
        return response

    def get_messages(self):
        return self.prompt["messages"]

    def set_messages(self, messages):
        self.msgs = messages
