import streamlit as st
from pathlib import Path
from rag.ingestion import DocumentLoader
from rag.chunking import TextChunker
from rag.embedding import EmbeddingManager
from rag.vector_store import FAISSVectorStore
from rag.retrieval import RAGRetriever
from rag.generation import RAGGenerator

# ----------------------
# Initialization
# ----------------------
embedding_manager = EmbeddingManager()
vector_store = FAISSVectorStore(embedding_dim=384)  # MiniLM embedding size
retriever = RAGRetriever(vector_store, embedding_manager)
generator = RAGGenerator(device="cpu")

# ----------------------
# UI Title
# ----------------------
st.title("📄 RAG QA System")

# ----------------------
# Document Upload Section
# ----------------------
uploaded_file = st.file_uploader(
    "Upload a document (PDF, DOCX, TXT)", 
    type=["pdf", "docx", "txt"]
)

if uploaded_file:
    # Save file to data folder
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)
    file_path = data_folder / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded {uploaded_file.name}")

    # Process the uploaded document
    loader = DocumentLoader(str(data_folder))
    docs = loader.load_documents()

    # Only process documents not already in FAISS
    existing_sources = {meta["source"] for meta in vector_store.metadata}
    new_docs = [doc for doc in docs if doc["source"] not in existing_sources]

    if new_docs:
        chunker = TextChunker()
        for doc in new_docs:
            doc["chunks"] = chunker.chunk_text(doc["text"])

        embeddings, metadata = embedding_manager.embed_documents(new_docs)
        vector_store.add_documents(embeddings, metadata)
        st.success(f"Indexed {len(new_docs)} new documents")
    else:
        st.info("Document already indexed")

# ----------------------
# Query Section
# ----------------------
query = st.text_input("Enter your question:")

if st.button("Get Answer") and query:
    context = retriever.retrieve(query)
    if context.strip() == "":
        st.warning("No relevant documents found. Please upload documents first.")
    else:
        answer = generator.generate_answer(context, query)
        st.subheader("Answer:")
        st.write(answer)
