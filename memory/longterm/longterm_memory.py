from rag.pipelines.security_rag_pipeline import SecurityRAGPipeline

class LongTermMemory:
    """Stores important facts in the vector store for long-term recall."""

    def __init__(self):
        self._rag = SecurityRAGPipeline()

    async def remember(self, fact: str, doc_id: str, metadata: dict = None):
        await self._rag.ingest(fact, doc_id, metadata)

    async def recall(self, query: str) -> str:
        return await self._rag.retrieve(query)
