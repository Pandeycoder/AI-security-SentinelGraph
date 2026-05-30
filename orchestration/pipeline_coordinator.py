"""
Pipeline Coordinator
Manages the full event-driven pipeline from Kafka event ingestion
through AI processing to final alert/audit output.
"""
from orchestration.workflow_orchestrator import WorkflowOrchestrator
from infrastructure.kafka.kafka_producer import KafkaEventProducer
from config.settings import settings
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


class PipelineCoordinator:
    """
    Coordinates the end-to-end security pipeline:
    Kafka Event → Workflow → Result → Audit Log → Notification Event
    """

    def __init__(self):
        self._orchestrator = WorkflowOrchestrator()
        self._producer = KafkaEventProducer()

    async def process_threat_event(self, event: dict) -> dict:
        logger.info(f"Processing threat event: {event.get('threat_id')}")
        result = await self._orchestrator.analyze_threat(
            threat_id=event.get("threat_id", str(uuid.uuid4())),
            source_ip=event.get("source_ip", "0.0.0.0"),
            threat_type=event.get("threat_type", "unknown"),
            description=event.get("description", ""),
        )
        await self._emit_audit_event(result)
        if result.get("status") == "success":
            await self._emit_notification_event(result)
        return result

    async def process_scan_event(self, event: dict) -> dict:
        logger.info(f"Processing scan event for URL: {event.get('url')}")
        result = await self._orchestrator.scan_website(url=event.get("url", ""))
        await self._emit_audit_event(result)
        return result

    async def _emit_audit_event(self, result: dict):
        audit_event = {
            "event_type": "PIPELINE_AUDIT",
            "pipeline_result": str(result.get("status")),
            "workflow": str(result.get("workflow", "unknown")),
            "timestamp": datetime.utcnow().isoformat(),
        }
        try:
            await self._producer.publish(settings.KAFKA_TOPIC_AUDIT, audit_event)
        except Exception as e:
            logger.warning(f"Failed to emit audit event: {e}")

    async def _emit_notification_event(self, result: dict):
        notif_event = {
            "event_type": "SECURITY_ALERT",
            "workflow": str(result.get("workflow")),
            "timestamp": datetime.utcnow().isoformat(),
        }
        try:
            await self._producer.publish(settings.KAFKA_TOPIC_NOTIFICATION, notif_event)
        except Exception as e:
            logger.warning(f"Failed to emit notification event: {e}")
