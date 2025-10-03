# rag/embedding.py

from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """Generate embeddings using SentenceTransformers."""

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list) -> list:
        embeddings = self.model.encode(texts, show_progress_bar=True)
        return [emb.tolist() for emb in embeddings]  # <-- convert to Python list
