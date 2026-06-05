def hybrid_search(bm25, bm25_chunks, collection, query, n_results=3):
    # 1. BM25 sonuçlarını al
    bm25_results = bm25.get_top_n(query.split(), bm25_chunks, n_results)
    # 2. Vector search sonuçlarını al
    vector_results = collection.query(query_texts=[query], n=n_results)
    # 3. İkisini birleştir (set veya dict ile duplicate'leri ele al)
    all_results = list(set(bm25_results + vector_results["documents"][0]))
    # 4. n_results kadar döndür
    return all_results[:n_results]
