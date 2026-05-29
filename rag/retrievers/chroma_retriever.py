from infrastructure.chromadb.vector_store import ChromaVectorStore

class ChromaRetriever:
    def __init__(self):
        self._store = ChromaVectorStore()

    def retrieve(self, embedding: list[float], top_k: int = 5) -> list[str]:
        return self._store.query(embedding, n_results=top_k)

    def add(self, id: str, document: str, embedding: list[float], metadata: dict):
        self._store.add_documents([id], [document], [embedding], [metadata])
