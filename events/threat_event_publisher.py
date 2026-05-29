from infrastructure.kafka.kafka_producer import KafkaEventProducer
from domain.entities.threat import Threat
from config.settings import settings
from datetime import datetime

class ThreatEventPublisher:
    def __init__(self):
        self._producer = KafkaEventProducer()

    async def publish(self, threat: Threat):
        event = {
            "event_type": "THREAT_DETECTED",
            "threat_id": threat.id,
            "source_ip": threat.source_ip,
            "level": threat.level.name,
            "risk_score": threat.risk_score,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await self._producer.publish(settings.KAFKA_TOPIC_THREAT_EVENTS, event)
