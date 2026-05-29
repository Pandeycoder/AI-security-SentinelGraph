from pydantic import BaseModel, Field

class ThreatCreateRequest(BaseModel):
    source_ip: str = Field(..., example="192.168.1.100")
    threat_type: str = Field(..., example="malware")
    level: str = Field(..., example="high")
    description: str = Field(..., min_length=10)
