"""
Validates the raw JSON dict returned by Gemini against the response schema.
"""

from __future__ import annotations

from app.exceptions import ResponseValidationError

# All fields that must be present in a valid Gemini response
REQUIRED_FIELDS: dict[str, type | tuple[type, ...]] = {
    "relevant_transaction_id": (str, type(None)),
    "evidence_verdict": str,
    "case_type": str,
    "severity": str,
    "department": str,
    "agent_summary": str,
    "recommended_next_action": str,
    "customer_reply": str,
    "human_review_required": bool,
    "confidence": (int, float),
    "reason_codes": list,
}


def validate_gemini_response(data: dict) -> dict:
    """
    Validate that the parsed Gemini JSON contains all required fields
    with correct types. Returns the validated dict.

    Raises ResponseValidationError on failure.
    """
    missing: list[str] = []
    type_errors: list[str] = []

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            missing.append(field)
            continue

        value = data[field]
        if not isinstance(value, expected_type):
            type_errors.append(
                f"{field}: expected {expected_type}, got {type(value).__name__}"
            )

    if missing:
        raise ResponseValidationError(f"Missing required fields: {', '.join(missing)}")

    if type_errors:
        raise ResponseValidationError(
            f"Type errors: {'; '.join(type_errors)}"
        )

    # Validate confidence range
    confidence = data["confidence"]
    if not (0.0 <= float(confidence) <= 1.0):
        raise ResponseValidationError(
            f"confidence must be between 0.0 and 1.0, got {confidence}"
        )

    # Normalize confidence to float
    data["confidence"] = float(data["confidence"])

    # Validate reason_codes contains only strings
    if not all(isinstance(code, str) for code in data["reason_codes"]):
        raise ResponseValidationError("reason_codes must be a list of strings")

    return data
