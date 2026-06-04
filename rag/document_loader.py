from pypdf import PdfReader


def read_pdf(pdf):
    reader = PdfReader(pdf)
    metin = ""
    for sayfa in reader.pages:
        metin += sayfa.extract_text()
    return metin


def chunking(metin, chunk_size=200, overlap=50):
    words = metin.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap
    return chunks
