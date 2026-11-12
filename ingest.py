import sys
from pathlib import Path

from rag import chunk, load_pdf


def main():
    if len(sys.argv) != 2:
        print("Usage: python ingest.py <path-to-pdf>")
        sys.exit(1)

    path = Path(sys.argv[1])
    pages = load_pdf(path)
    chunks = chunk(pages, source=path.name)

    empty = [p["page"] for p in pages if not p["text"].strip()]

    print(f"Pages:  {len(pages)}")
    if empty:
        print(f"Empty pages (no text layer, probably scanned): {empty}")
    print(f"Chunks: {len(chunks)}")

    if chunks:
        first = chunks[0]
        print(f"\n--- Chunk #0 | page {first['page']} | {len(first['text'])} chars ---")
        print(first["text"])


if __name__ == "__main__":
    main()