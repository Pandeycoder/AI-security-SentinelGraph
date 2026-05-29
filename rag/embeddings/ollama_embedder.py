from infrastructure.ollama.ollama_provider import OllamaProvider

class OllamaEmbedder:
    def __init__(self):
        self._provider = OllamaProvider()

    async def embed(self, text: str) -> list[float]:
        return await self._provider.embed(text)
