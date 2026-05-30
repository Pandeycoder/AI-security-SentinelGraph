"""
Document Indexer
Ingests security documents (CVEs, threat reports, policies) into the vector store.
Handles chunking, deduplication, and metadata tagging.
"""
from vectorstore.vector_store_manager import VectorStoreManager
from rag.chunking.text_chunker import TextChunker
from typing import List, Dict
import hashlib


class DocumentIndexer:
    def __init__(self):
        self._manager = VectorStoreManager()
        self._chunker = TextChunker(chunk_size=400, overlap=50)

    async def index_cve(self, cve_id: str, description: str, severity: str, affected_systems: List[str]):
        chunks = self._chunker.chunk(description)
        ids, texts, metas = [], [], []
        for i, chunk in enumerate(chunks):
            doc_id = f"{cve_id}_chunk_{i}"
            ids.append(doc_id)
            texts.append(chunk)
            metas.append({
                "cve_id": cve_id,
                "severity": severity,
                "type": "cve",
                "affected_systems": ", ".join(affected_systems),
                "chunk_index": i,
            })
        await self._manager.ingest_batch(texts, ids, collection="vulnerability_db", metadatas=metas)
        return len(chunks)

    async def index_threat_report(self, report_id: str, content: str, threat_actor: str = "unknown"):
        chunks = self._chunker.chunk(content)
        ids, texts, metas = [], [], []
        for i, chunk in enumerate(chunks):
            ids.append(f"{report_id}_chunk_{i}")
            texts.append(chunk)
            metas.append({"report_id": report_id, "threat_actor": threat_actor, "type": "threat_report", "chunk_index": i})
        await self._manager.ingest_batch(texts, ids, collection="security_knowledge", metadatas=metas)

    async def index_compliance_doc(self, standard: str, section: str, content: str):
        doc_id = hashlib.md5(f"{standard}:{section}".encode()).hexdigest()
        await self._manager.ingest_document(
            text=content,
            doc_id=doc_id,
            collection="compliance_docs",
            metadata={"standard": standard, "section": section, "type": "compliance"},
        )

    async def index_malware_signature(self, malware_id: str, family: str, description: str, iocs: List[str]):
        content = f"Malware Family: {family}\nDescription: {description}\nIOCs: {', '.join(iocs)}"
        await self._manager.ingest_document(
            text=content,
            doc_id=malware_id,
            collection="malware_signatures",
            metadata={"family": family, "malware_id": malware_id, "type": "malware_signature"},
        )
