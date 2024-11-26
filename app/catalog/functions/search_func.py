from fuzzywuzzy import process


def search_partial_match_fuzzy(
    text_list: list[str], query: str, threshold: int = 70
) -> list[str]:
    """Функция для поиска неполного совпадения с учетом ошибок в строках.

    Args:
        text_list (list[str]): Список строк для поиска
        query (str): Строка для поиска
        threshold (int, optional): Порог схожести (от 0 до 100). Defaults to 70.

    Returns:
        list[str]: Список строк, содержащих неполное совпадение
    """
    matches = process.extract(query, text_list, limit=None)
    return [text for text, score in matches if score >= threshold]
