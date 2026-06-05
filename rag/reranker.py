from sentence_transformers import CrossEncoder


def rerank(query, chunks, n_results=3):
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    # query ile her chunk'ı çift oluştur → [(query, chunk1), (query, chunk2)...]
    pairs = [[query, chunk] for chunk in chunks]
    # model.predict(pairs) ile skorları hesapla
    scores = model.predict(pairs)
    # skorlara göre sırala, en iyi n_results chunk'ı döndür
    sorted_list = sorted(zip(scores, chunks), reverse=True)
    return [chunk for score, chunk in sorted_list[:n_results]]
