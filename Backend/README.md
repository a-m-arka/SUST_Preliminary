# SUST Preliminary — AI Ticket Analyzer

A production-ready **FastAPI** service that analyzes customer financial complaint tickets using **Google Gemini AI**. Built for the SUST Preliminary Hackathon.

The service receives a complaint with transaction history, calls Gemini for investigation, validates the response, enforces safety rules, and returns a structured JSON verdict.

---

## Features

- 🤖 Gemini AI-powered complaint analysis
- 🔒 Safety rule enforcement (no PINs, OTPs, refund promises)
- 🔄 Automatic retry on malformed AI responses
- ✅ Full Pydantic validation on request and response
- 🛡️ No stack trace leakage — clean error responses
- 📄 Auto-generated API docs at `/docs`

---

## Project Structure

```
Backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   ├── config.py          # Environment configuration
│   ├── routes.py          # API route definitions
│   ├── schemas.py         # Pydantic models
│   ├── gemini_service.py  # Gemini API integration
│   ├── prompt_builder.py  # Prompt construction
│   ├── validator.py       # Response validation
│   ├── safety.py          # Safety rule enforcement
│   └── exceptions.py      # Custom exceptions & handlers
├── requirements.txt
├── .env.example
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.11+
- A Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

### Setup

```bash
# Clone the repo and navigate to Backend
cd Backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Environment Variables

Copy the example file and add your API key:

```bash
cp .env.example .env
```

Edit `.env`:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash
MAX_RETRIES=3
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ | — | Google Gemini API key |
| `GEMINI_MODEL` | ❌ | `gemini-2.0-flash` | Gemini model name |
| `MAX_RETRIES` | ❌ | `3` | Retry attempts for Gemini calls |

---

## Running Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or directly:

```bash
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## API Endpoints

### `GET /health`

Health check endpoint.

**Response** (HTTP 200):

```json
{
  "status": "ok"
}
```

---

### `POST /analyze-ticket`

Analyze a customer complaint using AI.

**Request Body:**

```json
{
  "ticket_id": "TKT-20250615-7890",
  "complaint": "I was charged twice for my electricity bill payment of 1500 BDT. I only intended to pay once but my account was debited twice on June 14th.",
  "language": "en",
  "channel": "app",
  "user_type": "premium",
  "campaign_context": null,
  "transaction_history": [
    {
      "transaction_id": "TXN-001",
      "timestamp": "2025-06-14T10:30:00Z",
      "type": "debit",
      "amount": 1500.00,
      "counterparty": "DPDC Electricity",
      "status": "success"
    },
    {
      "transaction_id": "TXN-002",
      "timestamp": "2025-06-14T10:30:05Z",
      "type": "debit",
      "amount": 1500.00,
      "counterparty": "DPDC Electricity",
      "status": "success"
    },
    {
      "transaction_id": "TXN-003",
      "timestamp": "2025-06-13T09:00:00Z",
      "type": "credit",
      "amount": 25000.00,
      "counterparty": "Employer Salary",
      "status": "success"
    }
  ],
  "metadata": {
    "app_version": "3.2.1",
    "device": "Android"
  }
}
```

**Response** (HTTP 200):

```json
{
  "ticket_id": "TKT-20250615-7890",
  "relevant_transaction_id": "TXN-002",
  "evidence_verdict": "supported",
  "case_type": "duplicate_charge",
  "severity": "high",
  "department": "billing_support",
  "agent_summary": "Customer reports duplicate debit of 1500 BDT for DPDC Electricity on June 14. Transaction history confirms two identical debits (TXN-001 and TXN-002) within 5 seconds, strongly suggesting a duplicate charge.",
  "recommended_next_action": "Initiate investigation for duplicate transaction TXN-002. Contact payment gateway for reversal confirmation.",
  "customer_reply": "Thank you for reaching out. We can see two identical charges of 1500 BDT to DPDC Electricity on June 14th. Our team is investigating this and will update you within 24-48 hours. Your case has been prioritized.",
  "human_review_required": true,
  "confidence": 0.92,
  "reason_codes": [
    "duplicate_transaction_detected",
    "same_counterparty",
    "identical_amount",
    "timestamp_proximity"
  ]
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Human-readable error message"
}
```

| Status Code | Meaning |
|---|---|
| 400 | Malformed request |
| 422 | Invalid request fields |
| 500 | Server / AI service error |

---

## Deployment

### Docker (optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment

The service is compatible with:
- **Railway** / **Render** — auto-detect via Procfile or `uvicorn` command
- **Google Cloud Run** — container-based
- **AWS Lambda** — via Mangum adapter

---

## Limitations

- No authentication — assumes trusted network or API gateway
- No database — results are not persisted
- Single-model dependency — relies on Gemini availability
- Safety rules use regex — not a full NLP safety classifier
- Synchronous Gemini calls within async endpoints (SDK limitation)
