import chromadb
import config

client = chromadb.PersistentClient(path=config.CHROMA_DB_DIRECTORY)

def get_collection():
    return client.get_or_create_collection(name="documents")

collection = get_collection()

def add_embeddings(texts, embeddings, sources):
    global collection
    ids = [f"{sources[i]}_{i}" for i in range(len(texts))]
    metadatas = [{"source": sources[i]} for i in range(len(texts))]
    collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)

def query_embedding(query_embedding, top_n=3):
    global collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n,
        include=["documents", "metadatas"]
    )
    return results

def collection_is_empty():
    global collection
    return collection.count() == 0

def clear_collection():
    global collection
    client.delete_collection(name="documents")
    collection = get_collection()  # <-- важлива зміна: переприсвоєння після видалення

def query_vector_db(query: str) -> str:
    # Повертає найрелевантніший текст для prompt
    return "Example extracted context from vector DB."
