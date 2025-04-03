from sentence_transformers import SentenceTransformer
import config

embedder = SentenceTransformer(config.EMBEDDINGS_MODEL_NAME)

def embed_texts(text_list):
    return embedder.encode(text_list)
