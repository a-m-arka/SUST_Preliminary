import json

from google import genai
from google.genai import types
from pydantic import ValidationError

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL
from app.schemas import (
    AnalyzeTicketRequest,
    GeminiResponse,
)

from .prompt import (
    SYSTEM_PROMPT,
    build_user_prompt,
)


class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def analyze_ticket(
        self,
        ticket: AnalyzeTicketRequest,
    ) -> GeminiResponse:

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=build_user_prompt(ticket),

            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,

                response_mime_type="application/json",

                temperature=0.2,
            ),
        )

        if response.text is None:
            raise ValueError("Gemini returned an empty response.")

        try:
            data = json.loads(response.text)

        except json.JSONDecodeError:
            raise ValueError("Gemini returned invalid JSON.")

        try:
            return GeminiResponse.model_validate(data)

        except ValidationError as e:
            raise ValueError(
                f"Gemini response validation failed:\n{e}"
            )


gemini_service = GeminiService()