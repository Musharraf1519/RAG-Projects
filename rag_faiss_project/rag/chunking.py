# chunking.py - add your code here
import re

class TextChunker:
    """Split text into smaller chunks suitable for embeddings."""

    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str):
        """Split text into overlapping chunks."""
        text = re.sub(r'\s+', ' ', text)
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.overlap
        return chunks
