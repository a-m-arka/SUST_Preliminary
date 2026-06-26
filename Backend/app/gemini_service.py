"""
Gemini API integration with retry logic.
"""

from __future__ import annotations

import json
import logging
import re

from google import genai
from google.genai import types

from app.config import settings
from app.exceptions import GeminiServiceError, ResponseValidationError
from app.prompt_builder import SYSTEM_PROMPT
from app.validator import validate_gemini_response

logger = logging.getLogger(__name__)

# Initialize client lazily
_client: genai.Client | None = None


def _get_client() -> genai.Client:
    """Lazily initialize the Gemini client."""
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise GeminiServiceError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def _extract_json(text: str) -> dict:
    """
    Extract JSON from Gemini's response text.
    Handles cases where the model wraps JSON in markdown code fences.
    """
    # Try direct parse first
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract from markdown code fences
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try to find a JSON object anywhere in the text
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    raise json.JSONDecodeError("No valid JSON found in response", text, 0)


async def call_gemini(user_prompt: str) -> dict:
    """
    Call Gemini with the system + user prompt.
    Retries up to MAX_RETRIES on JSON parse or validation failures.

    Returns a validated dict matching the response schema.
    Raises GeminiServiceError if all retries are exhausted.
    """
    client = _get_client()
    last_error: Exception | None = None

    for attempt in range(1, settings.MAX_RETRIES + 1):
        try:
            logger.info("Gemini call attempt %d/%d", attempt, settings.MAX_RETRIES)

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                    max_output_tokens=2048,
                ),
            )

            raw_text = response.text
            if not raw_text:
                raise GeminiServiceError("Gemini returned an empty response.")

            logger.debug("Gemini raw response: %s", raw_text[:500])

            # Parse and validate
            data = _extract_json(raw_text)
            validated = validate_gemini_response(data)
            return validated

        except (json.JSONDecodeError, ResponseValidationError) as e:
            logger.warning(
                "Attempt %d failed (retryable): %s", attempt, e
            )
            last_error = e
            continue

        except GeminiServiceError:
            raise

        except Exception as e:
            logger.error("Attempt %d failed (unexpected): %s", attempt, e)
            last_error = e
            continue

    raise GeminiServiceError(
        f"All {settings.MAX_RETRIES} Gemini attempts failed. Last error: {last_error}"
    )
