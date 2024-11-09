def split_into_pages(text: str, max_chars_per_page: int = 2000) -> list[str]:
    """Функция разбивает текст на страницы

    Args:
        text (str): Текст для разбиения
        max_chars_per_page (int, optional): Количество символов на одной странице. Defaults to 2000.

    Returns:
        list[str]: Список страниц
    """
    pages = []
    current_page = ""
    words = text.split()

    for word in words:
        if len(current_page) + len(word) > max_chars_per_page:
            pages.append(current_page.strip())
            current_page = word + " "
        else:
            current_page += word + " "

    if current_page:
        pages.append(current_page.strip())

    return pages
