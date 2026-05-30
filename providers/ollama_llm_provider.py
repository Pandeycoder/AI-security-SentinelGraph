"""
Ollama LLM Provider
Local LLM serving via Ollama (llama3, mistral, etc.)
Primary provider for air-gapped / on-premise enterprise deployments.
"""
import httpx
from domain.interfaces.llm_provider import ILLMProvider
from config.settings import settings
from observability.metrics import ai_latency
import time


class OllamaLLMProvider(ILLMProvider):
    def __init__(self, model: str = None, base_url: str = None):
        self.model = model or settings.OLLAMA_MODEL
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.timeout = 120.0

    async def generate(self, prompt: str, system: str = "") -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            "options": {"temperature": 0.1, "num_predict": 1024},
        }
        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
                response.raise_for_status()
                return response.json()["response"]
        finally:
            ai_latency.observe(time.perf_counter() - start)

    async def embed(self, text: str) -> list[float]:
        payload = {"model": self.model, "prompt": text}
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{self.base_url}/api/embeddings", json=payload)
            response.raise_for_status()
            return response.json()["embedding"]

    async def is_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(f"{self.base_url}/api/tags")
                return r.status_code == 200
        except Exception:
            return False
