"""
Vector Store Manager
High-level manager for all vector store operations.
Handles ingestion, retrieval, deletion, and collection stats.
"""
from vectorstore.chroma_store import ChromaStore
from providers.embedding_provider import EmbeddingProvider
from typing import List, Dict, Optional


class VectorStoreManager:
    def __init__(self):
        self._store = ChromaStore()
        self._embedder = EmbeddingProvider()

    async def ingest_document(
        self,
        text: str,
        doc_id: str,
        collection: str = "security_knowledge",
        metadata: Dict = None,
    ):
        """Embed and store a single document."""
        embedding = await self._embedder.embed_text(text)
        self._store.add(
            documents=[text],
            embeddings=[embedding],
            ids=[doc_id],
            metadatas=[metadata or {}],
            collection=collection,
        )

    async def ingest_batch(
        self,
        texts: List[str],
        ids: List[str],
        collection: str = "security_knowledge",
        metadatas: List[Dict] = None,
    ):
        """Embed and store multiple documents in one batch."""
        embeddings = await self._embedder.embed_batch(texts)
        self._store.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas or [{} for _ in texts],
            collection=collection,
        )

    async def search(
        self,
        query: str,
        collection: str = "security_knowledge",
        top_k: int = 5,
        filters: Dict = None,
    ) -> List[Dict]:
        """Semantic search — embed query then retrieve top-k results."""
        embedding = await self._embedder.embed_text(query)
        return self._store.query(embedding, n_results=top_k, collection=collection, where=filters)

    def delete_document(self, doc_id: str, collection: str = "security_knowledge"):
        self._store.delete([doc_id], collection=collection)

    def get_stats(self) -> Dict[str, int]:
        return {col: self._store.count(col) for col in self._store.list_collections()}
