import fitz
from pathlib import Path
import re
import config

def load_pdfs():
    docs = {}
    for pdf_file in Path(config.PDF_DIRECTORY).glob("*.pdf"):
        text = ""
        doc = fitz.open(pdf_file)
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        cleaned = re.sub(r'\s+', ' ', text).strip()
        docs[pdf_file.name] = cleaned
    return docs

def chunk_text(text, max_size=1000, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_size
        if end < len(text):
            end = text.rfind(' ', start, end)
            if end == -1:
                end = start + max_size
        chunks.append(text[start:end].strip())
        start = end - overlap
    return chunks
