from fastapi import FastAPI

from app.routes import (
    analyze_router,
    health_router,
)

app = FastAPI(
    title="QueueStorm Investigator API",
    description="AI/API SupportOps Challenge for Digital Finance",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(analyze_router)