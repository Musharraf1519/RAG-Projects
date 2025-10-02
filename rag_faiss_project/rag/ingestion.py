# ingestion.py - add your code here
import os
from pathlib import Path
from typing import List
import PyPDF2
import docx

class DocumentLoader:
    """Load PDFs, DOCX, and TXT files from a folder."""

    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    def load_documents(self) -> List[dict]:
        docs = []
        for file_path in Path(self.folder_path).glob("*"):
            if file_path.suffix.lower() == ".pdf":
                docs.append({"text": self._load_pdf(file_path), "source": str(file_path)})
            elif file_path.suffix.lower() == ".docx":
                docs.append({"text": self._load_docx(file_path), "source": str(file_path)})
            elif file_path.suffix.lower() == ".txt":
                docs.append({"text": self._load_txt(file_path), "source": str(file_path)})
        return docs

    def _load_pdf(self, file_path):
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _load_docx(self, file_path):
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    def _load_txt(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
