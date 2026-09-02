from dataclasses import dataclass
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    chunk_id: str
    title: str
    text: str


class KnowledgeBase:
    def __init__(self):
        self.chunks: list[Chunk] = []
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = None

    def add_document(self, title: str, content: str):
        words = content.split()
        size, overlap = 120, 25
        start = 0
        index = 0
        while start < len(words):
            text = " ".join(words[start:start + size]).strip()
            if text:
                self.chunks.append(Chunk(f"{len(self.chunks)+1}", title, text))
            index += 1
            start += size - overlap
        self.matrix = self.vectorizer.fit_transform([c.text for c in self.chunks])

    def retrieve(self, question: str, top_k: int = 3):
        if not self.chunks or self.matrix is None:
            return []
        query = self.vectorizer.transform([question])
        scores = cosine_similarity(query, self.matrix)[0]
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.chunks[i], float(score)) for i, score in ranked if score > 0]


class AnswerGenerator:
    def generate(self, question: str, results: list[tuple[Chunk, float]]) -> dict:
        if not results:
            return {"answer": "I could not find this information in the university knowledge base.", "sources": []}
        # Grounded extractive baseline: return the most relevant context.
        best = results[0][0]
        answer = f"Based on the university documents: {best.text}"
        sources = [{"chunk_id": c.chunk_id, "title": c.title, "score": round(score, 4)} for c, score in results]
        return {"answer": answer, "sources": sources}


kb = KnowledgeBase()
generator = AnswerGenerator()
