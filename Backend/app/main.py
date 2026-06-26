"""
FastAPI application entry point.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from app.exceptions import register_exception_handlers
from app.routes import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)

app = FastAPI(
    title="SUST Preliminary — AI Ticket Analyzer",
    description=(
        "A FastAPI service that analyzes customer complaint tickets using "
        "Google Gemini AI. Built for the SUST Preliminary Hackathon."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register global exception handlers
register_exception_handlers(app)

# Include API routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
