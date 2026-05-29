class SimpleReranker:
    def rerank(self, query: str, documents: list[str]) -> list[str]:
        query_words = set(query.lower().split())
        scored = []
        for doc in documents:
            doc_words = set(doc.lower().split())
            score = len(query_words & doc_words)
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored]
