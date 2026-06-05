def format_chunks_with_ids(chunks):
    satirlar = []
    for i, chunk in enumerate(chunks):
        satir = f"[chunk_{i}]: {chunk}"
        satirlar.append(satir)

    return "\n".join(satirlar)


def build_cited_prompt(query, formatted_chunks):
    return f"""
    Aşağıdaki kaynaklara dayanarak cevap ver.
    Her iddianda [Kaynak: chunk_id] şeklinde kaynak göster.
    Kaynaklar:
    {formatted_chunks}
    Soru: {query}
    """
