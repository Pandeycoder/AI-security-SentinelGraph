"""
OpenAI LLM Provider
Fallback / cloud provider using OpenAI-compatible API.
Used when Ollama is unavailable or for specific high-accuracy tasks.
"""
import httpx
from domain.interfaces.llm_provider import ILLMProvider
from observability.metrics import ai_latency
import time
import os


class OpenAILLMProvider(ILLMProvider):
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.base_url = "https://api.openai.com/v1"
        self.timeout = 60.0

    async def generate(self, prompt: str, system: str = "") -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {"model": self.model, "messages": messages, "max_tokens": 1024, "temperature": 0.1}
        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
        finally:
            ai_latency.observe(time.perf_counter() - start)

    async def embed(self, text: str) -> list[float]:
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": "text-embedding-3-small", "input": text}
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{self.base_url}/embeddings", headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]

    async def is_available(self) -> bool:
        return bool(self.api_key)
