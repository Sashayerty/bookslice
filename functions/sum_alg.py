import networkx as nx
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


def preprocess_text(text):
    sentences = sent_tokenize(text)
    return sentences


def summarize_text(text: str, compression_level: str = "weak") -> None:
    """Эта функция связывает в себе две функции.

    Args:
        text (str): Текст, который нужно сжать.
        compression_level (str, optional): Уровень сжатия. Есть два: 'strong' и 'weak'. Defaults to "weak".

    Returns:
        None: Просто связывает две функции.
    """
    sentences = preprocess_text(text)
    if compression_level == "strong":
        return strong_summary(sentences)
    elif compression_level == "weak":
        return weak_summary(sentences)


def weak_summary(sentences: list) -> str:
    """Функция weak_summary принимает список предложений и возвращает краткое содержание текста.
    Для этого она использует метод TF-IDF и алгоритм PageRank.

    Args:
        sentences (list): Список предложений текста


    Returns:
        str: Сжатый текст до примерно 3% от исходного.
    """
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    similarity_matrix = X * X.T
    nx_graph = nx.from_scipy_sparse_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = list(((scores[i], s) for i, s in enumerate(sentences)))
    n = 0
    while n < 3:
        dellist = []
        for i in range(0, len(ranked_sentences), 2):
            if len(ranked_sentences) > i + 1:
                first = ranked_sentences[i]
                second = ranked_sentences[i + 1]
                if first[0] > second[0]:
                    dellist.append(second)
                else:
                    dellist.append(first)
        for i in dellist:
            ranked_sentences.remove(i)
        n += 1
    summary = "\n".join([sent for _, sent in ranked_sentences])
    return summary


def strong_summary(sentences: list) -> str:
    """Функция strong_summary принимает список предложений и возвращает краткое содержание текста.
    Для этого она использует метод TF-IDF и алгоритм PageRank.

    Args:
        sentences (list): Список предложений текста

    Returns:
        str: Сжатый текст до примерно 1% от исходного.
    """
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    similarity_matrix = X * X.T
    nx_graph = nx.from_scipy_sparse_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = list(((scores[i], s) for i, s in enumerate(sentences)))
    n = 0
    while n < 6:
        dellist = []
        for i in range(0, len(ranked_sentences), 2):
            if len(ranked_sentences) > i + 1:
                first = ranked_sentences[i]
                second = ranked_sentences[i + 1]
                if first[0] > second[0]:
                    dellist.append(second)
                else:
                    dellist.append(first)
        for i in dellist:
            ranked_sentences.remove(i)
        n += 1
    summary = "\n".join([sent for _, sent in ranked_sentences])
    return summary
