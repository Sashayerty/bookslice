from langchain_text_splitters import RecursiveCharacterTextSplitter


def splitter(
    text: str,
    chunk_size: int,
) -> list[str]:
    """Функция для разделения текста на куски

    Args:
        text (str): Текст, который нужно разделить
        chunk_size (int): Размер кусков

    Returns:
        list[str]: Список кусков
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
        separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
            "\u200b",  # Zero-width space
            "\uff0c",  # Fullwidth comma
            "\u3001",  # Ideographic comma
            "\uff0e",  # Fullwidth full stop
            "\u3002",  # Ideographic full stop
            "",
        ],
    )
    splitted_text = text_splitter.split_text(text=text)
    return splitted_text


# print(*splitter(state_of_the_union, chunk_size=512), sep="\n\n")
