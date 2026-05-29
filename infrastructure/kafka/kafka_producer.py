import json
from aiokafka import AIOKafkaProducer
from config.settings import settings

class KafkaEventProducer:
    def __init__(self):
        self._producer: AIOKafkaProducer | None = None

    async def start(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self._producer.start()

    async def stop(self):
        if self._producer:
            await self._producer.stop()

    async def publish(self, topic: str, event: dict):
        if not self._producer:
            await self.start()
        await self._producer.send_and_wait(topic, event)
