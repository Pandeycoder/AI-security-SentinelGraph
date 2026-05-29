from rag.embeddings.ollama_embedder import OllamaEmbedder
from rag.retrievers.chroma_retriever import ChromaRetriever
from rag.reranking.simple_reranker import SimpleReranker
from rag.chunking.text_chunker import TextChunker

class SecurityRAGPipeline:
    def __init__(self):
        self._embedder = OllamaEmbedder()
        self._retriever = ChromaRetriever()
        self._reranker = SimpleReranker()

    async def retrieve(self, query: str, top_k: int = 5) -> str:
        embedding = await self._embedder.embed(query)
        docs = self._retriever.retrieve(embedding, top_k)
        reranked = self._reranker.rerank(query, docs)
        return "\n\n".join(reranked)

    async def ingest(self, text: str, doc_id: str, metadata: dict = None):
        chunker = TextChunker()
        chunks = chunker.chunk(text)
        for i, chunk in enumerate(chunks):
            embedding = await self._embedder.embed(chunk)
            self._retriever.add(
                id=f"{doc_id}_chunk_{i}",
                document=chunk,
                embedding=embedding,
                metadata=metadata or {},
            )
