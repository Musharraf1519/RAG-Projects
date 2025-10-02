import faiss
import numpy as np
import pickle
import os
from pathlib import Path

class FAISSVectorStore:
    """FAISS store with automatic incremental indexing."""

    def __init__(self, embedding_dim, index_path="embeddings/faiss_index"):
        self.index_path = Path(index_path)
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.metadata = []
        self._load_index_if_exists()

    def _load_index_if_exists(self):
        if self.index_path.with_suffix(".index").exists():
            self.index = faiss.read_index(str(self.index_path.with_suffix(".index")))
            with open(self.index_path.with_name(self.index_path.name + "_meta.pkl"), "rb") as f:
                self.metadata = pickle.load(f)
            print(f"[FAISS] Loaded existing index with {len(self.metadata)} vectors.")
        else:
            print("[FAISS] No existing index found. Starting fresh.")

    def add_documents(self, embeddings, metadata):
        """Add new embeddings incrementally."""
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.metadata.extend(metadata)
        self.save_index()
        print(f"[FAISS] Added {len(embeddings)} new vectors. Total now: {len(self.metadata)}.")

    def save_index(self):
        faiss.write_index(self.index, str(self.index_path.with_suffix(".index")))
        with open(self.index_path.with_name(self.index_path.name + "_meta.pkl"), "wb") as f:
            pickle.dump(self.metadata, f)

    def query(self, query_embedding, top_k=5):
        if len(self.metadata) == 0:
            return []
        distances, indices = self.index.search(np.array([query_embedding], dtype=np.float32), top_k)
        results = [self.metadata[i] for i in indices[0]]
        return results
