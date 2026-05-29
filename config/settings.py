from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Enterprise AI Security Platform"
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    # Database
    POSTGRES_URL: str = "postgresql+asyncpg://user:password@localhost:5432/ai_security"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_THREAT_EVENTS: str = "threat-events"
    KAFKA_TOPIC_SCAN_EVENTS: str = "scan-events"
    KAFKA_TOPIC_AI_ANALYSIS: str = "ai-analysis-events"
    KAFKA_TOPIC_AUDIT: str = "audit-events"
    KAFKA_TOPIC_NOTIFICATION: str = "notification-events"
    KAFKA_TOPIC_WORKFLOW: str = "workflow-events"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    # ChromaDB
    CHROMADB_HOST: str = "localhost"
    CHROMADB_PORT: int = 8000
    CHROMADB_COLLECTION: str = "security_knowledge"

    # JWT
    JWT_SECRET_KEY: str = "change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"

settings = Settings()
