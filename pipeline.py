import os
import hashlib
from dotenv import load_dotenv

from rag.document_loader import read_pdf, chunking
from rag.vector_store import get_or_create_index, upsert_chunks
from rag.bm25_retriever import create_bm25
from rag.hybrid_retriever import hybrid_search
from rag.reranker import rerank
from rag.citation_enforcer import format_chunks_with_ids, build_cited_prompt
from langchain_pipeline.graph import graph

load_dotenv()

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "cv-job-analyzer")


def _cv_namespace(cv_text: str) -> str:
    digest = hashlib.md5(cv_text.encode("utf-8")).hexdigest()[:16]
    return f"cv-{digest}"


def run_pipeline(cv_pdf_path, job_text, query="Genel Analiz"):
    # 1. PDF oku
    metin = read_pdf(cv_pdf_path)
    # 2. Chunk'la
    chunks = chunking(metin, 200, 50)
    # 3. Pinecone index + namespace
    namespace = _cv_namespace(metin)
    index = get_or_create_index(INDEX_NAME)
    upsert_chunks(index, chunks, namespace=namespace)
    # 4. BM25 lokal
    bm25 = create_bm25(chunks)
    # 5. Hybrid search + rerank
    results = hybrid_search(bm25, chunks, index, query, namespace=namespace)
    ranked = rerank(query, results)
    # 6. Citation prompt
    formatted = format_chunks_with_ids(ranked)
    cv_prompt = build_cited_prompt(query, formatted)
    # 7. LangGraph çalıştır
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
    # 8. Sonucu döndür
    return {
        "match": final_state["match_analysis"],
        "cover_letter": final_state["cover_letter"],
        "interview": final_state["interview_questions"],
        "gelisim": final_state["gelisim"],
    }
