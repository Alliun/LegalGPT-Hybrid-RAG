from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


# ==========================================
# Load Embedding Model
# ==========================================

print("\nLoading embedding model...")

model = SentenceTransformer(EMBEDDING_MODEL)

print("Embedding model loaded.\n")


# ==========================================
# Utility Functions
# ==========================================

def embed_text(text):

    return model.encode(
        text,
        normalize_embeddings=True
    ).tolist()


def embed_texts(texts):

    return model.encode(
        texts,
        normalize_embeddings=True
    ).tolist()