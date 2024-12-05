def join_text(text: list, sep: str = " ") -> str:
    """Соединяет список предложений в единый текст

    Args:
        text (list): Список предложений
        sep (str, optional): Разделитель. Defaults to " ".

    Returns:
        str: Строка - текст
    """
    return sep.join(text)
