from mistralai import Mistral
from dotenv import dotenv_values
from markdown import markdown

api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]


class AI:
    def __init__(self) -> None:
        self.client = Mistral(api_key=api_key)
        self.msgs = []
        self.promt = {'messages': self.msgs}

    def message(self, mess):
        self.msgs.append({"role": "user", "text": mess})
        self.promt["messages"] = self.msgs
        self.chat_response = self.client.chat.complete(
            model = "mistral-large-latest",
            messages = [
                {
                    "role": "user",
                    "content": f"""Ты - ИИ помощник для сайта-соцсети, посвещённой чтению. Ты должен поддерживать диалог, нейтрально относясь к острым темам, и выдавать сухую информацию о них:
                    религия, политика, национальность. Ответы должны быть ТОЛЬКО на русском. История сообщений с юзером:{self.msgs}""",
                },
            ]
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
