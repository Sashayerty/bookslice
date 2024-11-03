from random import choice

import networkx as nx
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


def summarize_text(text: str, compression_level: str = "weak") -> str:
    """Функция принимает текст и возвращает краткое содержание текста.
    Для этого она использует метод TF-IDF и алгоритм PageRank.

    Args:
        text (str): Текст, который нужно сжать.
        compression_level (str, optional): Уровень сжатия. Есть два: "strong" и "weak". Defaults to "weak".

    Returns:
        str: Сжатый текст до примерно 6% (weak) или 1% (strong) от исходного.
    """
    sentences = sent_tokenize(text)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    similarity_matrix = X * X.T
    nx_graph = nx.from_scipy_sparse_array(similarity_matrix)
    scores = nx.pagerank(nx_graph)
    ranked_sentences = list(((scores[i], s) for i, s in enumerate(sentences)))
    # Определяем важность слов в каждом предложении с помощью TF-IDF векторов
    if compression_level == "strong":
        return sorted(ranked_sentences)[-1][1]
        # При сильном сжатии выдаём самое важное предложение
    for j in range(5):
        # При слабом сжатии проходимся по предложениям и из двух оставляем более важное
        # Количество сокращений на половину - 5 раз, т.е 6% +- рандом
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
            # Менее важные предложения могут остаться с шансом 25%
            if choice([1, 1, 1, 0]) == 1:
                ranked_sentences.remove(i)
    summary = "\n".join([sent for _, sent in ranked_sentences])
    return summary
