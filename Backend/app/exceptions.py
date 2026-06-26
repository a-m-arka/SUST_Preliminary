"""
Custom exceptions and FastAPI exception handlers.
All error responses use {"error": "message"} format.
Stack traces are never exposed to clients.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


# ── Custom Exceptions ───────────────────────────────────────────────────────


class GeminiServiceError(Exception):
    """Raised when the Gemini API call fails after all retries."""

    pass


class SafetyViolationError(Exception):
    """Raised when the AI-generated customer reply violates safety rules."""

    pass


class ResponseValidationError(Exception):
    """Raised when the Gemini response fails schema validation."""

    pass


# ── Exception Handlers ──────────────────────────────────────────────────────


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the FastAPI app."""

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """422 — semantically invalid request body."""
        logger.warning("Validation error: %s", exc.errors())
        return JSONResponse(
            status_code=422,
            content={"error": "Invalid request: " + _summarize_validation(exc)},
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        _request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """Handle generic HTTP exceptions (400, 404, etc.)."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": str(exc.detail)},
        )

    @app.exception_handler(GeminiServiceError)
    async def gemini_error_handler(
        _request: Request, _exc: GeminiServiceError
    ) -> JSONResponse:
        """500 — Gemini API failure."""
        logger.error("Gemini service error: %s", _exc)
        return JSONResponse(
            status_code=500,
            content={"error": "AI service is temporarily unavailable. Please retry."},
        )

    @app.exception_handler(SafetyViolationError)
    async def safety_error_handler(
        _request: Request, _exc: SafetyViolationError
    ) -> JSONResponse:
        """500 — AI produced unsafe content that could not be sanitized."""
        logger.error("Safety violation: %s", _exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": "AI response did not meet safety requirements. Please retry."
            },
        )

    @app.exception_handler(ResponseValidationError)
    async def response_validation_handler(
        _request: Request, _exc: ResponseValidationError
    ) -> JSONResponse:
        """500 — Gemini returned structurally invalid data."""
        logger.error("Response validation error: %s", _exc)
        return JSONResponse(
            status_code=500,
            content={"error": "AI returned an invalid response. Please retry."},
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(
        _request: Request, exc: Exception
    ) -> JSONResponse:
        """500 — catch-all so stack traces never leak."""
        logger.exception("Unexpected error: %s", exc)
        return JSONResponse(
            status_code=500,
            content={"error": "An unexpected error occurred."},
        )


def _summarize_validation(exc: RequestValidationError) -> str:
    """Build a human-readable summary from validation errors."""
    messages: list[str] = []
    for err in exc.errors():
        loc = " → ".join(str(part) for part in err.get("loc", []))
        messages.append(f"{loc}: {err.get('msg', 'invalid')}")
    return "; ".join(messages[:5])  # cap at 5 for readability
