from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from .transaction import Transaction


class AnalyzeTicketRequest(BaseModel):
    ticket_id: str

    complaint: str = Field(
        ...,
        min_length=1,
    )

    language: Optional[
        Literal[
            "en",
            "bn",
            "mixed",
        ]
    ] = None

    channel: Optional[
        Literal[
            "in_app_chat",
            "call_center",
            "email",
            "merchant_portal",
            "field_agent",
        ]
    ] = None

    user_type: Optional[
        Literal[
            "customer",
            "merchant",
            "agent",
            "unknown",
        ]
    ] = None

    campaign_context: Optional[str] = None

    transaction_history: List[Transaction] = []

    metadata: Optional[dict] = None