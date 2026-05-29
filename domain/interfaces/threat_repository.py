from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.threat import Threat

class IThreatRepository(ABC):
    @abstractmethod
    async def save(self, threat: Threat) -> Threat: ...

    @abstractmethod
    async def find_by_id(self, threat_id: str) -> Optional[Threat]: ...

    @abstractmethod
    async def find_all(self, limit: int = 50) -> List[Threat]: ...

    @abstractmethod
    async def update(self, threat: Threat) -> Threat: ...

    @abstractmethod
    async def delete(self, threat_id: str) -> None: ...
