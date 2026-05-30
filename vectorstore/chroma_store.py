"""
ChromaDB Vector Store — Primary vector database for RAG and semantic search.
Collections:
  - security_knowledge  : CVEs, threat intel, security docs
  - malware_signatures  : malware family patterns
  - incident_reports    : historical incident data
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from config.settings import settings
from typing import List, Dict, Optional
import uuid


class ChromaStore:
    COLLECTIONS = {
        "security_knowledge": "Security intelligence, CVEs, threat reports",
        "malware_signatures": "Malware family signatures and behavioral patterns",
        "incident_reports":   "Historical security incident records",
        "compliance_docs":    "Security standards: NIST, ISO 27001, CIS Controls",
        "vulnerability_db":   "Known vulnerability database",
    }

    def __init__(self):
        self._client = chromadb.HttpClient(
            host=settings.CHROMADB_HOST,
            port=settings.CHROMADB_PORT,
        )
        self._collections: Dict[str, chromadb.Collection] = {}
        self._init_collections()

    def _init_collections(self):
        for name in self.COLLECTIONS:
            self._collections[name] = self._client.get_or_create_collection(
                name=name,
                metadata={"description": self.COLLECTIONS[name]},
            )

    def add(
        self,
        documents: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict] = None,
        ids: List[str] = None,
        collection: str = "security_knowledge",
    ):
        col = self._collections.get(collection)
        if not col:
            raise ValueError(f"Unknown collection: {collection}")
        col.add(
            ids=ids or [str(uuid.uuid4()) for _ in documents],
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas or [{} for _ in documents],
        )

    def query(
        self,
        embedding: List[float],
        n_results: int = 5,
        collection: str = "security_knowledge",
        where: Dict = None,
    ) -> List[Dict]:
        col = self._collections.get(collection)
        if not col:
            return []
        kwargs = {"query_embeddings": [embedding], "n_results": n_results}
        if where:
            kwargs["where"] = where
        results = col.query(**kwargs)
        output = []
        for i, doc in enumerate(results["documents"][0]):
            output.append({
                "document": doc,
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results.get("distances") else 0.0,
                "id": results["ids"][0][i],
            })
        return output

    def delete(self, ids: List[str], collection: str = "security_knowledge"):
        col = self._collections.get(collection)
        if col:
            col.delete(ids=ids)

    def count(self, collection: str = "security_knowledge") -> int:
        col = self._collections.get(collection)
        return col.count() if col else 0

    def list_collections(self) -> List[str]:
        return list(self.COLLECTIONS.keys())
