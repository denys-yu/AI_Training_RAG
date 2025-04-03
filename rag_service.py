import embeddings
import vector_db
import llm_service

def retrieve_context(query, top_n=3):
    q_embedding = embeddings.embed_texts([query])[0]
    results = vector_db.query_embedding(q_embedding, top_n)
    context_texts = results["documents"][0]
    sources = [meta["source"] for meta in results["metadatas"][0]]
    return context_texts, sources

def answer_question(query):
    contexts, sources = retrieve_context(query)
    context = "\n".join(contexts)

    prompt = f"""
    You are an assistant answering questions based on the provided context below.

    Context:
    {context}

    Question: {query}
    Answer:
    """

    #  prompt = (
  #      f"Ти – асистент, що відповідає на запитання, спираючись на наведений контекст:\n"
  #      f"{context}\n"
  #      f"Запит: {query}\nВідповідь українською:"
  #  )
    answer = llm_service.generate_response(prompt)
    return answer, sources
