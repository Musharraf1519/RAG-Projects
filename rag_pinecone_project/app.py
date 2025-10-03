import os
import streamlit as st
from rag.ingestion import DataIngestor
from rag.chunking import Chunker
from rag.embedding import EmbeddingGenerator
from rag.vector_db import PineconeDB
from rag.retriever import RAGRetriever
from rag.generator import LLMGenerator

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="BrainWave 🧠 RAG Q&A", layout="wide")
st.title("🧠 BrainWave: Smart Document Q&A")

# ---------------------- Config ----------------------
DATA_DIR = "data/"
INDEX_NAME = "rag-demo"
VECTOR_DIM = 384

os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------- Initialize Modules ----------------------
ingestor = DataIngestor(DATA_DIR)
chunker = Chunker()
embedder = EmbeddingGenerator()
vector_db = PineconeDB(INDEX_NAME, VECTOR_DIM)
retriever = RAGRetriever(vector_db, embedder)
generator = LLMGenerator()

# ---------------------- File Upload ----------------------
st.subheader("📂 Upload Documents")
uploaded_files = st.file_uploader(
    "Upload TXT, PDF, or DOCX files", type=["txt", "pdf", "docx"], accept_multiple_files=True
)

if uploaded_files:
    for f in uploaded_files:
        path = os.path.join(DATA_DIR, f.name)
        with open(path, "wb") as out:
            out.write(f.getbuffer())
    st.success(f"✅ {len(uploaded_files)} files uploaded!")

# ---------------------- Document Ingestion ----------------------
if st.button("🚀 Ingest & Index Documents"):
    documents = ingestor.load_all_documents()
    if not documents:
        st.warning("No documents found in the data folder.")
    else:
        for doc in documents:
            chunks = chunker.chunk_text(doc['content'])
            embeddings = embedder.embed(chunks)  # returns list
            vectors = [(f"{doc['name']}_{i}", emb, {"text": chunks[i]}) 
                       for i, emb in enumerate(embeddings)]
            vector_db.upsert(vectors)
        st.success("✅ Documents ingested and indexed!")

# ---------------------- Query Interface ----------------------
st.subheader("💬 Ask Questions")
query = st.text_input("Ask me anything about your documents:")

if query:
    context = retriever.retrieve(query)
    answer = generator.generate(context, query)
    st.markdown("**Answer:**")
    st.info(answer)
