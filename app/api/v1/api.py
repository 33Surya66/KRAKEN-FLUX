from fastapi import APIRouter
from .endpoints import agents, evidence, metrics, system

api_router = APIRouter()

# Register all endpoint routers
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(evidence.router, prefix="/evidence", tags=["evidence"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(system.router, prefix="/system", tags=["system"]) 