# ingestion.py - add your code here
# rag/ingestion.py
import os
from typing import List
from docx import Document
import PyPDF2

class DataIngestor:
    """Handles loading documents from disk."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def load_docx(self, file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def load_pdf(self, file_path: str) -> str:
        pdf_text = []
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                pdf_text.append(page.extract_text())
        return "\n".join(pdf_text)

    def load_all_documents(self) -> List[dict]:
        """Load all documents in data_dir and return list of dicts: [{'name':..., 'content':...}]"""
        documents = []
        for filename in os.listdir(self.data_dir):
            path = os.path.join(self.data_dir, filename)
            ext = filename.split('.')[-1].lower()
            if ext == 'txt':
                content = self.load_txt(path)
            elif ext == 'docx':
                content = self.load_docx(path)
            elif ext == 'pdf':
                content = self.load_pdf(path)
            else:
                continue
            documents.append({'name': filename, 'content': content})
        return documents
