# retrieval.py - add your code here
class RAGRetriever:
    """Combine embeddings and FAISS retrieval for RAG."""

    def __init__(self, vector_store, embedding_manager, top_k=5):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager
        self.top_k = top_k

    def retrieve(self, query: str):
        query_embedding = self.embedding_manager.embed_query(query)
        top_chunks = self.vector_store.query(query_embedding, top_k=self.top_k)
        # Combine chunks into a single context string
        context = "\n".join([chunk["text"] for chunk in top_chunks])
        return context
