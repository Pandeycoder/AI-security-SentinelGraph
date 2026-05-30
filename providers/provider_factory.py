"""
LLM Provider Factory
Selects the best available provider based on config and availability.
Strategy: prefer Ollama (local/private), fall back to OpenAI.
"""
from domain.interfaces.llm_provider import ILLMProvider
from providers.ollama_llm_provider import OllamaLLMProvider
from providers.openai_llm_provider import OpenAILLMProvider
from config.settings import settings


class LLMProviderFactory:
    _instance: ILLMProvider = None

    @classmethod
    async def get_provider(cls) -> ILLMProvider:
        """Returns a live provider. Ollama first, OpenAI as fallback."""
        if cls._instance:
            return cls._instance

        ollama = OllamaLLMProvider()
        if await ollama.is_available():
            cls._instance = ollama
            return ollama

        openai = OpenAILLMProvider()
        if await openai.is_available():
            cls._instance = openai
            return openai

        # Last resort: return Ollama anyway (it may come online later)
        return ollama

    @classmethod
    def reset(cls):
        """Force re-evaluation on next call (e.g. after config change)."""
        cls._instance = None
