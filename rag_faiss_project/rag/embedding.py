# embedding.py - add your code here
from sentence_transformers import SentenceTransformer

class EmbeddingManager:
    """Generate embeddings using Sentence-Transformers."""

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, docs):
        """
        Input: List of dicts {"text": ..., "source": ...}
        Output: List of embeddings and metadata
        """
        embeddings = []
        metadata = []
        for doc in docs:
            chunks = doc["chunks"]
            for chunk in chunks:
                embeddings.append(self.model.encode(chunk))
                metadata.append({"source": doc["source"], "text": chunk})
        return embeddings, metadata

    def embed_query(self, query: str):
        return self.model.encode(query)
