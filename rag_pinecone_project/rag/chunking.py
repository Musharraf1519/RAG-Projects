# rag/chunking.py

import re
from typing import List

class Chunker:
    """Split documents into chunks with overlap."""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def clean_text(self, text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()

    def chunk_text(self, text: str) -> List[str]:
        text = self.clean_text(text)
        words = text.split(' ')
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunks.append(' '.join(words[start:end]))
            start += self.chunk_size - self.overlap
        return chunks
