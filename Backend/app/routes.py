"""
API route definitions.
Only two endpoints: GET /health and POST /analyze-ticket.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter

from app.gemini_service import call_gemini
from app.prompt_builder import build_user_prompt
from app.safety import check_safety
from app.schemas import AnalyzeTicketRequest, AnalyzeTicketResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


@router.post("/analyze-ticket", response_model=AnalyzeTicketResponse)
async def analyze_ticket(request: AnalyzeTicketRequest) -> AnalyzeTicketResponse:
    """
    Analyze a customer complaint ticket using Gemini AI.

    1. Build prompt from request data
    2. Call Gemini (with retries)
    3. Validate the AI response
    4. Enforce safety rules on customer_reply
    5. Return structured response
    """
    logger.info("Analyzing ticket: %s", request.ticket_id)

    # Build the prompt
    user_prompt = build_user_prompt(request)

    # Call Gemini (includes validation via gemini_service)
    ai_result = await call_gemini(user_prompt)

    # Enforce safety rules on customer_reply
    check_safety(ai_result["customer_reply"])

    # Build and return the response
    response = AnalyzeTicketResponse(
        ticket_id=request.ticket_id,
        relevant_transaction_id=ai_result["relevant_transaction_id"],
        evidence_verdict=ai_result["evidence_verdict"],
        case_type=ai_result["case_type"],
        severity=ai_result["severity"],
        department=ai_result["department"],
        agent_summary=ai_result["agent_summary"],
        recommended_next_action=ai_result["recommended_next_action"],
        customer_reply=ai_result["customer_reply"],
        human_review_required=ai_result["human_review_required"],
        confidence=ai_result["confidence"],
        reason_codes=ai_result["reason_codes"],
    )

    logger.info(
        "Ticket %s analyzed — verdict: %s, severity: %s",
        request.ticket_id,
        response.evidence_verdict,
        response.severity,
    )

    return response
