from prometheus_client import Counter, Histogram, Gauge

threats_detected = Counter("threats_detected_total", "Total threats detected", ["level"])
ai_latency = Histogram("ai_inference_seconds", "AI inference latency")
active_workflows = Gauge("active_workflows", "Currently running LangGraph workflows")
rag_retrievals = Counter("rag_retrievals_total", "Total RAG retrieval calls")
kafka_lag = Gauge("kafka_consumer_lag", "Kafka consumer lag", ["topic"])
