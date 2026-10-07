import json
import os
import re

DATA_FOLDER = "./data"
CHUNKS_FILE = os.path.join(DATA_FOLDER, "chunks.json")

class TextChunk:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

class FastRetriever:
    """Ultra-lightweight keyword and relevance retriever.
    Runs entirely in memory with 0 MB extra RAM — zero PyTorch needed."""
    def __init__(self, chunks):
        self.chunks = chunks

    def invoke(self, query):
        if not self.chunks:
            return []

        # Extract search keywords (minimum 3 characters)
        words = [w.lower() for w in re.findall(r'[a-zA-Z]{3,}', query)]
        if not words:
            # Default to top overview pages
            return [
                TextChunk(
                    c['content'],
                    {'source': 'GWRA2022_Report.pdf', 'page': c['page']}
                )
                for c in self.chunks[:3]
            ]

        scored = []
        for c in self.chunks:
            text = c['content'].lower()
            score = sum(text.count(w) for w in words)
            if score > 0:
                scored.append((score, c))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:4] if scored else [(0, c) for c in self.chunks[:2]]

        return [
            TextChunk(
                item[1]['content'],
                {'source': 'GWRA2022_Report.pdf', 'page': item[1]['page']}
            )
            for item in top
        ]

_retriever = None

def get_retriever():
    """Load pre-extracted CGWB report chunks into FastRetriever."""
    global _retriever
    if _retriever is not None:
        return _retriever

    chunks = []
    if os.path.exists(CHUNKS_FILE):
        try:
            with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
                chunks = json.load(f)
            print(f"[RAG] FastRetriever loaded {len(chunks)} report pages instantly.")
        except Exception as e:
            print(f"[RAG] Error loading chunks.json: {e}")
    else:
        print(f"[RAG] chunks.json not found at {CHUNKS_FILE}.")

    _retriever = FastRetriever(chunks)
    return _retriever