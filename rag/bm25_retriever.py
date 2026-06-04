from rank_bm25 import BM25Okapi


def create_bm25(chunks):
    # her chunk'ı kelimelere böl
    tokenized_chunk = [chunk.split() for chunk in chunks]
    # BM25Okapi objesi oluştur
    bm25 = BM25Okapi(tokenized_chunk)
    # return et
    return bm25


def query_bm25(bm25, chunks, query, n_results=3):
    # query'yi tokenize et
    query = query.split()
    # skorları hesapla → bm25.get_scores(tokens)
    score = bm25.get_scores(query)
    # en yüksek n_results chunk'ı döndür
    results = bm25.get_top_n(query, chunks, n_results)
    return results
