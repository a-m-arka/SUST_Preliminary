"""
Pydantic models for request and response schemas.
Strictly follows the SUST Preliminary Hackathon problem statement.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


# ── Request Models ──────────────────────────────────────────────────────────


class Transaction(BaseModel):
    """A single financial transaction from the user's history."""

    transaction_id: str
    timestamp: datetime
    type: str = Field(
        ..., description="Transaction type, e.g. debit, credit, transfer"
    )
    amount: float
    counterparty: str
    status: str = Field(
        ..., description="Transaction status, e.g. success, failed, pending"
    )


class AnalyzeTicketRequest(BaseModel):
    """Incoming complaint ticket with transaction history."""

    ticket_id: str
    complaint: str
    language: str
    channel: str = Field(..., description="Channel, e.g. app, web, call")
    user_type: str = Field(..., description="User type, e.g. premium, standard")
    campaign_context: str | None = None
    transaction_history: list[Transaction]
    metadata: dict[str, Any] | None = None


# ── Response Models ─────────────────────────────────────────────────────────


class AnalyzeTicketResponse(BaseModel):
    """AI-generated analysis result for a complaint ticket."""

    ticket_id: str
    relevant_transaction_id: str | None
    evidence_verdict: str = Field(
        ...,
        description="e.g. supported, unsupported, inconclusive",
    )
    case_type: str = Field(
        ...,
        description="e.g. fraud, dispute, technical_error",
    )
    severity: str = Field(
        ...,
        description="e.g. low, medium, high, critical",
    )
    department: str
    agent_summary: str
    recommended_next_action: str
    customer_reply: str
    human_review_required: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason_codes: list[str]
