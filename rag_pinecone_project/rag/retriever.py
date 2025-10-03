# rag/retriever.py
class RAGRetriever:
    """Retrieve relevant chunks for a query."""

    def __init__(self, vector_db, embedding_generator):
        self.vector_db = vector_db
        self.embedding_generator = embedding_generator

    def retrieve(self, query: str, top_k: int = 5) -> str:
        query_vector = self.embedding_generator.embed([query])[0]
        if hasattr(query_vector, "tolist"):
            query_vector = query_vector.tolist()
        results = self.vector_db.query(query_vector, top_k=top_k)
        chunks = [match['metadata']['text'] for match in results['matches']]
        return " ".join(chunks)
