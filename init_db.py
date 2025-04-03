import pdf_processor
import embeddings
import vector_db


def build_db():
    print("📄 Завантаження PDF-документів...")
    docs = pdf_processor.load_pdfs()

    texts = []
    sources = []
    for source, content in docs.items():
        chunks = pdf_processor.chunk_text(content)
        texts.extend(chunks)
        sources.extend([source] * len(chunks))

    print(f"🔢 Створення ембеддингів ({len(texts)} фрагментів)...")
    embeds = embeddings.embed_texts(texts)

    print("🗃️ Запис у векторну БД...")
    vector_db.clear_collection()  # очищуємо перед новим записом
    vector_db.add_embeddings(texts, embeds, sources)

    print(f"✅ Векторна БД створена. Всього {len(texts)} записів.")


if __name__ == "__main__":
    build_db()
