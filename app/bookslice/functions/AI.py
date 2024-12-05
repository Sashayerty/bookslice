import requests
from dotenv import dotenv_values
from markdown import markdown
from mistralai import Mistral

api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]


class AI:
    def __init__(self) -> None:
        self.client = Mistral(api_key=api_key)
        self.msgs = []
        self.promt = {"messages": self.msgs}

    def message(self, mess, user_id):
        response = requests.get(
            f"http://127.0.0.1:5000/get-user-data-for-ai?user_id={user_id}"
        ).text
        print(response)
        self.msgs.append({"role": "user", "text": mess})
        self.promt["messages"] = self.msgs
        self.chat_response = self.client.chat.complete(
            model="mistral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": f"""Ты - ИИ помощник для сайта-соцсети, посвящённой чтению. Ты должен
                    поддерживать диалог, нейтрально относясь к острым темам. Ответы должны быть
                    ТОЛЬКО на русском. Не делай таблицы.
                    Тебе данные с помощью json файла{response}. all_books_in_cataloh - все книги в каталоге с названием и автором
                    которые следует советовать во время диалога. readed_books_by_user - книги, прочитанные юзером
                    user_data_common - общая информация по юзеру. История сообщений с юзером:{self.msgs}""",
                },
            ],
        )
        response = markdown(self.chat_response.choices[0].message.content)
        self.promt["messages"].append(
            {
                "role": "assistant",
                "text": response,
            }
        )
        return response

    def get_messages(self):
        return self.promt["messages"]

    def set_messages(self, messages):
        self.msgs = messages
