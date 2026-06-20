from rag.document_loader import read_pdf, chunking
from rag.vector_store import create_vector_store
from rag.bm25_retriever import create_bm25
from rag.hybrid_retriever import hybrid_search
from rag.reranker import rerank
from rag.citation_enforcer import format_chunks_with_ids, build_cited_prompt
from langchain_pipeline.graph import graph


def run_pipeline(cv_pdf_path, job_text, query="Genel Analiz"):
    # 1. PDF oku
    metin = read_pdf(cv_pdf_path)
    # 2. Chunk'la
    chunks = chunking(metin, 200, 50)
    # 3. Vector store + BM25 oluştur
    collection = create_vector_store(chunks)
    bm25 = create_bm25(chunks)
    # 4. Hybrid search + rerank
    results = hybrid_search(bm25, chunks, collection, query)
    ranked = rerank(query, results)
    # 5. Citation prompt oluştur
    formatted = format_chunks_with_ids(ranked)
    cv_prompt = build_cited_prompt(query, formatted)
    # 6. LangGraph çalıştır
    initial_state = {
        "cv_text": cv_prompt,
        "job_text": job_text,
        "cv_analysis": {},
        "job_analysis": {},
        "match_analysis": {},
        "cover_letter": "",
        "interview_questions": {},
        "gelisim": "",
    }
    final_state = graph.invoke(initial_state)
    # 7. Sonucu döndür
    return {
        "match": final_state["match_analysis"],
        "cover_letter": final_state["cover_letter"],
        "interview": final_state["interview_questions"],
        "gelisim": final_state["gelisim"],
    }
