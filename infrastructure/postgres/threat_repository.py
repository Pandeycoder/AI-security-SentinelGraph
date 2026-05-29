from typing import List, Optional
from domain.entities.threat import Threat
from domain.interfaces.threat_repository import IThreatRepository

class PostgresThreatRepository(IThreatRepository):
    """SQLAlchemy async implementation — wire up engine in production."""

    async def save(self, threat: Threat) -> Threat:
        # TODO: async session.add(ThreatModel.from_entity(threat))
        return threat

    async def find_by_id(self, threat_id: str) -> Optional[Threat]:
        # TODO: query by id
        return None

    async def find_all(self, limit: int = 50) -> List[Threat]:
        # TODO: query all
        return []

    async def update(self, threat: Threat) -> Threat:
        return threat

    async def delete(self, threat_id: str) -> None:
        pass
