# Enterprise AI Security Platform — AI Service

FastAPI + LangGraph AI platform for enterprise security intelligence.

## Architecture

```
api/          → Thin REST controllers (no business logic)
application/  → Use cases (orchestrate domain + infra)
domain/       → Pure business logic (no framework deps)
infrastructure/ → DB, Redis, Kafka, Ollama, ChromaDB
graph/        → LangGraph workflow nodes + builders
agents/       → AI agents (threat, review, recommendation, citation, compliance)
rag/          → RAG pipeline (chunking, embed, retrieve, rerank, cite)
memory/       → Session + long-term memory
security/     → JWT, prompt injection guard
observability/ → Prometheus metrics
events/       → Kafka event publishers
config/       → Settings + environment
tests/        → Unit + integration tests
```

## Quick Start

```bash
cp .env.example .env
docker-compose up -d
uvicorn main:app --reload
```

## API Docs
Visit http://localhost:8000/docs

## Key Endpoints
- POST /api/v1/threats/analyze   → Analyze a threat with AI
- POST /api/v1/scan/website      → Scan a URL for malicious activity
- POST /api/v1/security/ask      → Ask a security question (RAG-powered)
- GET  /health                   → Health check
- GET  /metrics                  → Prometheus metrics
