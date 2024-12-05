import json

from dotenv import dotenv_values
from mistralai import Mistral


def generate_test(text: str):
    """Функция для генерации тестов

    Keyword arguments:
    text -- Текст, по которому надо сгенерить
    """

    api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    format = """
    {
        "1": {
            "question": "Сколько лет главному герою?",
            "choices": {
                "1": "12",
                "2": "13",
                "3": "18"
            },
            "right_answer": "1"
        }
    }
    """
    chat_response = client.chat.complete(
        model="pixtral-large-latest",
        messages=[
            {
                "role": "user",
                "content": f"""Составь тест по произведению {text}.
                В нем должно быть РОВНО 5 вопросов. Твой ответ должен иметь такой формат:
                {format}. Это если что пример.""",
            },
        ],
        response_format={
            "type": "json_object",
        },
    )
    return json.loads(chat_response.choices[0].message.content)


# print(generate_test(text=text))

# with open("test.json", "w", encoding="utf-8") as f:
#     f.write(generate_test(text=text))
