"""
🧪 API Test Script — SUST Preliminary Backend
Run korар আগে server চালু করো: python -m uvicorn app.main:app --reload --port 8000
তারপর এটা run করো: python test_api.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_header(text):
    print(f"\n{'='*60}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{'='*60}")


def print_result(label, status, detail=""):
    icon = f"{GREEN}✅ PASS{RESET}" if status else f"{RED}❌ FAIL{RESET}"
    print(f"  {icon}  {label}")
    if detail:
        print(f"        {YELLOW}{detail}{RESET}")


# ─────────────────────────────────────────────────────────────
# TEST 1: Health Check
# ─────────────────────────────────────────────────────────────
def test_health():
    print_header("TEST 1: GET /health")
    try:
        r = requests.get(f"{BASE_URL}/health")
        data = r.json()
        print_result("Status Code = 200", r.status_code == 200, f"Got: {r.status_code}")
        print_result('Response = {{"status": "ok"}}', data == {"status": "ok"}, f"Got: {data}")
    except Exception as e:
        print_result("Connection", False, str(e))


# ─────────────────────────────────────────────────────────────
# TEST 2: Analyze Ticket — Full Valid Request
# ─────────────────────────────────────────────────────────────
def test_analyze_ticket():
    print_header("TEST 2: POST /analyze-ticket (Valid Request)")

    payload = {
        "ticket_id": "TKT-20250615-7890",
        "complaint": "I was charged twice for my electricity bill payment of 1500 BDT. I only intended to pay once but my account was debited twice on June 14th.",
        "language": "en",
        "channel": "app",
        "user_type": "premium",
        "campaign_context": None,
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

    try:
        print(f"  {YELLOW}⏳ Sending request to Gemini (may take 5-15 seconds)...{RESET}")
        r = requests.post(f"{BASE_URL}/analyze-ticket", json=payload, timeout=60)
        print_result("Status Code = 200", r.status_code == 200, f"Got: {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            print(f"\n  {BOLD}📋 Response:{RESET}")
            print(f"  {json.dumps(data, indent=2, ensure_ascii=False)}")

            # Validate all required fields
            required_fields = [
                "ticket_id", "relevant_transaction_id", "evidence_verdict",
                "case_type", "severity", "department", "agent_summary",
                "recommended_next_action", "customer_reply",
                "human_review_required", "confidence", "reason_codes"
            ]

            print(f"\n  {BOLD}🔍 Field Validation:{RESET}")
            for field in required_fields:
                present = field in data
                print_result(f"{field}", present, f"Value: {data.get(field, 'MISSING')}" if present else "MISSING!")

            # Check confidence range
            if "confidence" in data:
                conf = data["confidence"]
                print_result("confidence in [0.0, 1.0]", 0.0 <= conf <= 1.0, f"Value: {conf}")

            # Check types
            if "human_review_required" in data:
                print_result("human_review_required is bool", isinstance(data["human_review_required"], bool))

            if "reason_codes" in data:
                print_result("reason_codes is list", isinstance(data["reason_codes"], list))

        else:
            print(f"  {RED}Error Response: {r.text}{RESET}")

    except requests.exceptions.Timeout:
        print_result("Request", False, "Timeout after 60 seconds")
    except Exception as e:
        print_result("Request", False, str(e))


# ─────────────────────────────────────────────────────────────
# TEST 3: Missing Required Fields — Should return 422
# ─────────────────────────────────────────────────────────────
def test_missing_fields():
    print_header("TEST 3: POST /analyze-ticket (Missing Fields → 422)")

    payload = {
        "ticket_id": "TKT-BAD-001"
        # complaint, language, channel, user_type, transaction_history — সব missing
    }

    try:
        r = requests.post(f"{BASE_URL}/analyze-ticket", json=payload)
        print_result("Status Code = 422", r.status_code == 422, f"Got: {r.status_code}")
        data = r.json()
        print_result('"error" key in response', "error" in data, f"Got: {data}")
    except Exception as e:
        print_result("Request", False, str(e))


# ─────────────────────────────────────────────────────────────
# TEST 4: Malformed JSON — Should return 422
# ─────────────────────────────────────────────────────────────
def test_bad_json():
    print_header("TEST 4: POST /analyze-ticket (Bad JSON → 422)")

    try:
        r = requests.post(
            f"{BASE_URL}/analyze-ticket",
            data="this is not json{{{",
            headers={"Content-Type": "application/json"}
        )
        print_result("Status Code = 422", r.status_code == 422, f"Got: {r.status_code}")
        data = r.json()
        print_result('"error" key in response', "error" in data, f"Got: {data}")
    except Exception as e:
        print_result("Request", False, str(e))


# ─────────────────────────────────────────────────────────────
# TEST 5: Empty Transaction History
# ─────────────────────────────────────────────────────────────
def test_empty_transactions():
    print_header("TEST 5: POST /analyze-ticket (Empty Transaction History)")

    payload = {
        "ticket_id": "TKT-EMPTY-001",
        "complaint": "My account balance seems incorrect. I think I was overcharged somewhere.",
        "language": "en",
        "channel": "web",
        "user_type": "standard",
        "campaign_context": None,
        "transaction_history": [],
        "metadata": None
    }

    try:
        print(f"  {YELLOW}⏳ Sending request to Gemini...{RESET}")
        r = requests.post(f"{BASE_URL}/analyze-ticket", json=payload, timeout=60)
        print_result(f"Status Code = {r.status_code}", r.status_code in [200, 500], f"Got: {r.status_code}")

        data = r.json()
        if r.status_code == 200:
            print_result("ticket_id matches", data.get("ticket_id") == "TKT-EMPTY-001")
            print(f"  {BOLD}📋 Response:{RESET}")
            print(f"  {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"  {YELLOW}ℹ️  Error (acceptable for empty history): {data}{RESET}")

    except Exception as e:
        print_result("Request", False, str(e))


# ─────────────────────────────────────────────────────────────
# TEST 6: Bangla Complaint
# ─────────────────────────────────────────────────────────────
def test_bangla_complaint():
    print_header("TEST 6: POST /analyze-ticket (Bangla Complaint)")

    payload = {
        "ticket_id": "TKT-BN-001",
        "complaint": "আমার একাউন্ট থেকে ১০০০ টাকা কেটে নেওয়া হয়েছে কিন্তু আমি কোনো লেনদেন করিনি। দয়া করে সাহায্য করুন।",
        "language": "bn",
        "channel": "app",
        "user_type": "standard",
        "campaign_context": None,
        "transaction_history": [
            {
                "transaction_id": "TXN-BN-001",
                "timestamp": "2025-06-14T15:00:00Z",
                "type": "debit",
                "amount": 1000.00,
                "counterparty": "Unknown Merchant",
                "status": "success"
            }
        ],
        "metadata": None
    }

    try:
        print(f"  {YELLOW}⏳ Sending Bangla complaint to Gemini...{RESET}")
        r = requests.post(f"{BASE_URL}/analyze-ticket", json=payload, timeout=60)
        print_result(f"Status Code = {r.status_code}", r.status_code == 200, f"Got: {r.status_code}")

        if r.status_code == 200:
            data = r.json()
            print(f"\n  {BOLD}📋 Response:{RESET}")
            print(f"  {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"  {RED}Error: {r.text}{RESET}")

    except Exception as e:
        print_result("Request", False, str(e))


# ─────────────────────────────────────────────────────────────
# RUN ALL TESTS
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n{BOLD}{CYAN}🚀 SUST Preliminary — API Test Suite{RESET}")
    print(f"{YELLOW}   Server: {BASE_URL}{RESET}")
    print(f"{YELLOW}   Make sure the server is running!{RESET}")

    # Quick tests (no Gemini call)
    test_health()
    test_missing_fields()
    test_bad_json()

    # Gemini tests (need API key, takes time)
    print(f"\n{BOLD}{CYAN}🤖 Gemini Integration Tests (needs valid API key){RESET}")
    test_analyze_ticket()
    test_empty_transactions()
    test_bangla_complaint()

    print(f"\n{'='*60}")
    print(f"{BOLD}{GREEN}  ✅ All tests completed!{RESET}")
    print(f"{'='*60}\n")
