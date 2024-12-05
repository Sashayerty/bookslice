from dotenv import dotenv_values
from mistralai import Mistral
from split_text_into_chunks import splitter


def summarizer(text: str) -> list[str]:
    """Сжимает текст по кусочкам

    Keyword arguments:
    text -- Текст, который надо сжать
    Return: summarized_text: list[str] -- Сжатый текст
    """

    api_key = dotenv_values("./.env")["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)
    splitted_text = splitter(text=text, chunk_size=1024)
    summarized_text = []
    for text in splitted_text:
        prompt = f"""Ты — мощный литературный компрессор текста, который сжимает текст без потери смысла.
        Твоя задача — сократить следующий текст ровно в 4 раза,
        сохранив все ключевые идеи и важную информацию.
        Убедись, что сокращенный текст остается понятным и информативным.
        Оригинальный текст:
        {text}"""
        summarized_chunk = client.chat.complete(
            model="pixtral-large-latest",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        response = summarized_chunk.choices[0].message.content
        summarized_text.append(response)
    return summarized_text


# print(summarizer(text=text))
