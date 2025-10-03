# rag/vector_db.py
import os
from pinecone import Pinecone, ServerlessSpec

class PineconeDB:
    """Wrapper for Pinecone SDK using environment variable API key."""

    def __init__(self, index_name: str, vector_dim: int):
        # Read API key from environment variable
        api_key = os.environ.get("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is not set!")

        # Initialize Pinecone client
        self.pc = Pinecone(api_key=api_key)

        # Choose cloud and region (free-tier defaults)
        cloud = "aws"        # could also be "gcp" or "azure"
        region = "us-east-1"  # adjust if you prefer another free region

        # Create index if not exists
        existing_indexes = [i["name"] for i in self.pc.list_indexes()]
        if index_name not in existing_indexes:
            self.pc.create_index(
                name=index_name,
                dimension=vector_dim,
                metric="cosine",
                spec=ServerlessSpec(cloud=cloud, region=region)  # Required
            )

        # Connect to index
        self.index = self.pc.Index(index_name)

    def upsert(self, vectors: list):
        """Insert embeddings into Pinecone index."""
        self.index.upsert(vectors=vectors)

    def query(self, vector, top_k: int = 5):
        """Retrieve top-k most similar vectors."""
        return self.index.query(vector=vector, top_k=top_k, include_metadata=True)
