import chromadb
from config.settings import settings

class ChromaVectorStore:
    def __init__(self):
        self._client = chromadb.HttpClient(
            host=settings.CHROMADB_HOST,
            port=settings.CHROMADB_PORT,
        )
        self._collection = self._client.get_or_create_collection(
            name=settings.CHROMADB_COLLECTION
        )

    def add_documents(self, ids: list, documents: list, embeddings: list, metadatas: list = None):
        self._collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas or [{} for _ in ids],
        )

    def query(self, embedding: list, n_results: int = 5) -> list[str]:
        results = self._collection.query(query_embeddings=[embedding], n_results=n_results)
        return results["documents"][0] if results["documents"] else []
