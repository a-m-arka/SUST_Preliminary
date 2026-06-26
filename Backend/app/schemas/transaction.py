from typing import Literal

from pydantic import BaseModel


class Transaction(BaseModel):
    transaction_id: str
    timestamp: str

    type: Literal[
        "transfer",
        "payment",
        "cash_in",
        "cash_out",
        "settlement",
        "refund",
    ]

    amount: float

    counterparty: str

    status: Literal[
        "completed",
        "failed",
        "pending",
        "reversed",
    ]