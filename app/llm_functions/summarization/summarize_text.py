import json

import requests


def split_text_into_chunks(text, chunk_size):
    """
    Разбивает текст на чанки заданного размера.

    :param text: Строка текста, которую нужно разбить.
    :param chunk_size: Размер каждого чанка в символах.
    :return: Список чанков.
    """
    if chunk_size <= 0:
        raise ValueError("Размер чанка должен быть положительным числом.")

    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i : i + chunk_size])

    return chunks


def send_chunk_to_server(chunk):
    """
    Отправляет чанк текста на сервер и возвращает ответ.

    :param chunk: Чанк текста для отправки.
    :return: Ответ от сервера.
    """
    url = "http://10.25.70.231:8852/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "qilowoq/Vikhr-Nemo-12B-Instruct-R-21-09-24-4Bit-GPTQ",
        "messages": [
            {
                "role": "system",
                "content": """Ты — мощный литературный компрессор текста, который сжимает текст без потери смысла. 
        Твоя задача — сократить следующий текст ровно в 4 раза, 
        сохранив все ключевые идеи и важную информацию. 
        Убедись, что сокращенный текст остается понятным и информативным. 
        В ответе пиши только сжатый текст. 
        Не пиши в ответе лишнюю информацию. 
 
        """,
            },
            {"role": "user", "content": chunk},
        ],
        # "min_tokens": 250,
        # "max_tokens": 1024,
        "temperature": 0.3,
        # "top_p": 0.95,
        # "top_k": 10,
        # "frequency_penalty": 0.0,
        # "presence_penalty": 0.0,
        # "n": 1,
        # "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def combine_responses(responses):
    """
    Объединяет несколько ответов в один.

    :param responses: Список ответов от сервера.
    :return: Объединенный ответ.
    """
    combined_response = ""
    for response in responses:
        combined_response += (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            + "\n"
        )
    return combined_response


# Пример использования


def summarizer(text: str) -> str:
    chunk_size = 1096  # Размер каждого чанка в символах
    chunks = split_text_into_chunks(text, chunk_size)

    responses = []
    for chunk in chunks:
        response = send_chunk_to_server(chunk)
        responses.append(response)

    combined_response = combine_responses(responses)
    return f"{combined_response}"
