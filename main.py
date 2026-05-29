from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import threat_router, scan_router, security_router, health_router
from observability.setup import setup_observability
from config.settings import settings

app = FastAPI(
    title="Enterprise AI Security Platform",
    version="1.0.0",
    description="AI-powered security platform with LangGraph workflows",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router.router, prefix="/health", tags=["Health"])
app.include_router(threat_router.router, prefix="/api/v1/threats", tags=["Threats"])
app.include_router(scan_router.router, prefix="/api/v1/scan", tags=["Scan"])
app.include_router(security_router.router, prefix="/api/v1/security", tags=["Security"])

setup_observability(app)

@app.on_event("startup")
async def startup():
    print("AI Security Platform starting...")

@app.on_event("shutdown")
async def shutdown():
    print("AI Security Platform shutting down...")
