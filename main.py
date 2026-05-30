from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import threat_router, scan_router, security_router, health_router
from api.routes import orchestration_router
from observability.setup import setup_observability
from config.settings import settings

app = FastAPI(
    title="Enterprise AI Security Platform",
    version="1.0.0",
    description="AI-powered security platform with LangGraph workflows, RAG, and multi-agent orchestration",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core API routes
app.include_router(health_router.router,       prefix="/health",            tags=["Health"])
app.include_router(threat_router.router,       prefix="/api/v1/threats",    tags=["Threats"])
app.include_router(scan_router.router,         prefix="/api/v1/scan",       tags=["Scan"])
app.include_router(security_router.router,     prefix="/api/v1/security",   tags=["Security"])

# Orchestration routes (workflows + multi-agent pipelines)
app.include_router(orchestration_router.router, prefix="/api/v1/orchestrate", tags=["Orchestration"])

setup_observability(app)

@app.on_event("startup")
async def startup():
    print("🛡️  Enterprise AI Security Platform starting...")
    print("📡 Workflows: ThreatAnalysis | WebsiteScan | PasswordAudit | MalwareAnalysis | RAGQuery")
    print("🤖 Agents: Threat | Review | Recommendation | Citation | Compliance")
    print("🔍 Docs: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown():
    print("AI Security Platform shutting down...")
