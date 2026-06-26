from fastapi import APIRouter, HTTPException

from app.schemas import (
    AnalyzeTicketRequest,
    AnalyzeTicketResponse,
)

from app.services.gemini import gemini_service
from app.utils.safety import validate_response

router = APIRouter(tags=["Analyze"])


@router.post(
    "/analyze-ticket",
    response_model=AnalyzeTicketResponse,
)
async def analyze_ticket(
    request: AnalyzeTicketRequest,
):
    try:
        # Ask Gemini to analyze the ticket
        gemini_response = gemini_service.analyze_ticket(request)

        # Apply safety validation
        validated_response = validate_response(gemini_response)

        # Build final response
        return AnalyzeTicketResponse(
            ticket_id=request.ticket_id,
            relevant_transaction_id=validated_response.relevant_transaction_id,
            evidence_verdict=validated_response.evidence_verdict,
            case_type=validated_response.case_type,
            severity=validated_response.severity,
            department=validated_response.department,
            agent_summary=validated_response.agent_summary,
            recommended_next_action=validated_response.recommended_next_action,
            customer_reply=validated_response.customer_reply,
            human_review_required=validated_response.human_review_required,
            confidence=validated_response.confidence,
            reason_codes=validated_response.reason_codes,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        )