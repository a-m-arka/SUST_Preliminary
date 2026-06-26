from app.schemas import GeminiResponse


FORBIDDEN_REQUESTS = [
    "provide your otp",
    "share your otp",
    "enter your otp",
    "send your otp",
    "tell me your otp",
    "give me your otp",

    "provide your pin",
    "share your pin",
    "enter your pin",
    "tell me your pin",

    "provide your password",
    "share your password",
    "tell me your password",

    "provide your cvv",
    "share your cvv",

    "provide your full card number",
    "share your full card number",
]

PROMISE_PHRASES = [
    "we will refund",
    "refund will be processed",
    "we guarantee refund",
    "your money will be returned",
    "we will reverse",
    "we have reversed",
    "your account has been recovered",
]


def contains_forbidden_request(text: str) -> bool:
    text = text.lower()

    return any(
        phrase in text
        for phrase in FORBIDDEN_REQUESTS
    )


def contains_unauthorized_promise(text: str) -> bool:
    text = text.lower()

    return any(
        phrase in text
        for phrase in PROMISE_PHRASES
    )


def validate_response(response: GeminiResponse) -> GeminiResponse:
    """
    Sanitizes Gemini responses instead of raising exceptions.
    """

    if contains_forbidden_request(response.customer_reply):
        response.customer_reply = (
            "For your security, never share confidential credentials such as "
            "OTP, PIN, passwords, CVV, or full card numbers with anyone."
        )

    if contains_forbidden_request(response.recommended_next_action):
        response.recommended_next_action = (
            "Verify the customer's identity using approved internal procedures "
            "without requesting confidential credentials."
        )

    if contains_unauthorized_promise(response.customer_reply):
        response.customer_reply = (
            "We understand your concern. Our team will review your case and "
            "inform you once the investigation is complete."
        )

    if contains_unauthorized_promise(response.recommended_next_action):
        response.recommended_next_action = (
            "Investigate the case according to internal procedures and update "
            "the customer after verification."
        )

    if (
        response.relevant_transaction_id is None
        and response.evidence_verdict != "insufficient_data"
    ):
        response.evidence_verdict = "insufficient_data"

    return response