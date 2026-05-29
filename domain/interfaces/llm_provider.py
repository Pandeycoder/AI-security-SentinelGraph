from abc import ABC, abstractmethod

class ILLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system: str = "") -> str: ...

    @abstractmethod
    async def embed(self, text: str) -> list[float]: ...
