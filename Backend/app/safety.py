"""
Safety rule enforcement for AI-generated customer replies.

Scans the customer_reply field for forbidden patterns and sanitizes
or rejects unsafe content.
"""

from __future__ import annotations

import re
import logging

from app.exceptions import SafetyViolationError

logger = logging.getLogger(__name__)

# ── Forbidden Patterns ──────────────────────────────────────────────────────
# Each tuple: (compiled regex, human-readable description)

_FORBIDDEN_PATTERNS: list[tuple[re.Pattern, str]] = [
    # Asking for sensitive credentials
    (
        re.compile(r"\b(provide|share|send|give|enter|confirm|verify)\b.*\b(pin|otp)\b", re.IGNORECASE),
        "Asks for PIN or OTP",
    ),
    (
        re.compile(r"\b(provide|share|send|give|enter|confirm|verify)\b.*\bpassword\b", re.IGNORECASE),
        "Asks for password",
    ),
    (
        re.compile(r"\b(provide|share|send|give|enter|confirm|verify)\b.*\b(card\s*number|full\s*card)\b", re.IGNORECASE),
        "Asks for full card number",
    ),
    (
        re.compile(r"\bask\w*\s+(for\s+)?(your\s+)?(pin|otp|password|card\s*number)\b", re.IGNORECASE),
        "Asks for sensitive information",
    ),
    # Direct requests for credentials
    (
        re.compile(r"\byour\s+(pin|otp|password)\b", re.IGNORECASE),
        "References user's PIN/OTP/password",
    ),
    # Promising outcomes
    (
        re.compile(r"\b(we\s+will|we\'ll|i\s+will|i\'ll|we\s+can|guaranteed)\b.*\b(refund|reverse|reversal)\b", re.IGNORECASE),
        "Promises refund or reversal",
    ),
    (
        re.compile(r"\b(promise|guaranteed?|assured?|certainly\s+will)\b.*\b(refund|revers|recover)\b", re.IGNORECASE),
        "Promises financial action",
    ),
    (
        re.compile(r"\b(we\s+will|we\'ll|i\s+will|i\'ll)\b.*\b(recover\s+your\s+account|restore\s+your\s+account)\b", re.IGNORECASE),
        "Promises account recovery",
    ),
    # Unofficial channels
    (
        re.compile(r"\b(whatsapp|telegram|facebook\s*messenger|dm\s+us|direct\s+message)\b", re.IGNORECASE),
        "Recommends unofficial support channel",
    ),
    (
        re.compile(r"\b(contact|reach|message)\s+us\s+(on|via|through)\s+(social\s+media|twitter|instagram)\b", re.IGNORECASE),
        "Recommends unofficial support channel",
    ),
]


def check_safety(customer_reply: str) -> str:
    """
    Check the customer_reply for safety violations.

    Returns the reply unchanged if safe.
    Raises SafetyViolationError if unsafe content is detected.
    """
    violations: list[str] = []

    for pattern, description in _FORBIDDEN_PATTERNS:
        if pattern.search(customer_reply):
            violations.append(description)

    if violations:
        logger.warning(
            "Safety violations detected in customer_reply: %s",
            "; ".join(violations),
        )
        raise SafetyViolationError(
            f"Customer reply contains unsafe content: {'; '.join(violations)}"
        )

    return customer_reply
