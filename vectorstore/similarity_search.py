"""
Similarity Search
Advanced search capabilities: hybrid search, cross-collection search, threshold filtering.
"""
from vectorstore.vector_store_manager import VectorStoreManager
from typing import List, Dict


class SimilaritySearch:
    DEFAULT_THRESHOLD = 0.7

    def __init__(self):
        self._manager = VectorStoreManager()

    async def search_all_collections(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search across all collections and merge results."""
        collections = ["security_knowledge", "malware_signatures", "vulnerability_db", "compliance_docs"]
        all_results = []
        for col in collections:
            results = await self._manager.search(query, collection=col, top_k=top_k)
            for r in results:
                r["collection"] = col
            all_results.extend(results)
        all_results.sort(key=lambda x: x.get("distance", 1.0))
        return all_results[:top_k * 2]

    async def find_similar_threats(self, threat_description: str, top_k: int = 5) -> List[Dict]:
        return await self._manager.search(
            query=threat_description,
            collection="security_knowledge",
            top_k=top_k,
        )

    async def find_malware_family(self, behavior_description: str) -> List[Dict]:
        return await self._manager.search(
            query=behavior_description,
            collection="malware_signatures",
            top_k=3,
        )

    async def find_compliance_guidance(self, topic: str, standard: str = None) -> List[Dict]:
        filters = {"standard": standard} if standard else None
        return await self._manager.search(
            query=topic,
            collection="compliance_docs",
            top_k=5,
            filters=filters,
        )
