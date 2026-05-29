import httpx
from domain.interfaces.llm_provider import ILLMProvider
from config.settings import settings

class OllamaProvider(ILLMProvider):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    async def generate(self, prompt: str, system: str = "") -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "system": system,
                "stream": False,
            }
            response = await client.post(f"{self.base_url}/api/generate", json=payload)
            response.raise_for_status()
            return response.json()["response"]

    async def embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {"model": self.model, "prompt": text}
            response = await client.post(f"{self.base_url}/api/embeddings", json=payload)
            response.raise_for_status()
            return response.json()["embedding"]
