from rag.vector_store import query_similar


def hybrid_search(bm25, bm25_chunks, index, query, namespace, n_results=3):
    # 1. BM25 sonuçlarını al (lokal, hızlı)
    bm25_results = bm25.get_top_n(query.split(), bm25_chunks, n_results)
    # 2. Pinecone'dan semantic sonuçlar
    vector_results = query_similar(index, query, namespace, top_k=n_results)
    # 3. Duplicate'leri ele (set sırayı bozar, ama rerank zaten yeniden sıralayacak)
    all_results = list(set(bm25_results + vector_results))
    # 4. n_results kadar döndür
    return all_results[:n_results]
