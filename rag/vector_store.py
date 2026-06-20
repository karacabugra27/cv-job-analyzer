import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings

load_dotenv()

_EMBED_MODEL = "text-embedding-3-small"
_EMBED_DIM = 1536

_embeddings = OpenAIEmbeddings(model=_EMBED_MODEL)
_pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


def get_or_create_index(index_name: str):
    existing = [idx["name"] for idx in _pc.list_indexes()]
    if index_name not in existing:
        _pc.create_index(
            name=index_name,
            dimension=_EMBED_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        while not _pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
    return _pc.Index(index_name)


def upsert_chunks(index, chunks: list[str], namespace: str):
    stats = index.describe_index_stats()
    ns_info = stats.get("namespaces", {}).get(namespace)
    if ns_info and ns_info.get("vector_count", 0) >= len(chunks):
        return

    vectors_raw = _embeddings.embed_documents(chunks)
    payload = [
        {
            "id": f"chunk_{i}",
            "values": vec,
            "metadata": {"text": chunks[i]},
        }
        for i, vec in enumerate(vectors_raw)
    ]
    index.upsert(vectors=payload, namespace=namespace)


def query_similar(index, query: str, namespace: str, top_k: int = 3) -> list[str]:
    query_vec = _embeddings.embed_query(query)
    res = index.query(
        vector=query_vec,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True,
    )
    return [match["metadata"]["text"] for match in res["matches"]]
