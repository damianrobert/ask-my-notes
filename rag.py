from pypdf import PdfReader

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def load_pdf(path):
    """Read a PDF and return one {"page", "text"} dict per page, numbered from 1."""
    reader = PdfReader(path)
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({"page": number, "text": text})
    return pages


def chunk(pages, source, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split each page's text into overlapping chunks. Chunks never cross pages."""
    step = size - overlap
    chunks = []
    for page in pages:
        text = page["text"].strip()
        if not text:
            continue
        for start in range(0, len(text), step):
            chunks.append({
                "id": f"{source}-p{page['page']}-c{start}",
                "text": text[start:start + size],
                "source": source,
                "page": page["page"],
            })
            if start + size >= len(text):
                break
    return chunks