"""
Embedding Provider
Handles vector embeddings for RAG, semantic search, and similarity matching.
"""
from domain.interfaces.llm_provider import ILLMProvider
from providers.ollama_llm_provider import OllamaLLMProvider
from typing import List


class EmbeddingProvider:
    def __init__(self, llm: ILLMProvider = None):
        self._llm = llm or OllamaLLMProvider()

    async def embed_text(self, text: str) -> List[float]:
        return await self._llm.embed(text)

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            emb = await self._llm.embed(text)
            embeddings.append(emb)
        return embeddings

    async def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        mag_a = sum(a ** 2 for a in vec_a) ** 0.5
        mag_b = sum(b ** 2 for b in vec_b) ** 0.5
        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)
