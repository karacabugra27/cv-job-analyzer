import chromadb


def create_vector_store(chunks, collection_name="cv_chunks"):

    chroma_client = chromadb.Client()

    collection = chroma_client.get_or_create_collection(collection_name)

    ids = [f"chunk_{i}" for i, _ in enumerate(chunks)]
    documents = chunks

    collection.add(
        ids=ids,
        documents=documents,
    )

    return collection


def query_vector_store(collection, query, n_results=3):
    results = collection.query(query_texts=[query], n_results=n_results)
    return results["documents"][0]
