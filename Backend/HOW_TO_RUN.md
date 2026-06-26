# 🚀 কিভাবে Run করবে — Step by Step

---

## Step 1: Terminal Open করো

VS Code তে Terminal open করো (`Ctrl + ~`) অথবা PowerShell/CMD open করো।

---

## Step 2: Backend ফোল্ডারে যাও

```bash
cd "f:\fluuter project\SUST_Preliminary\Backend"
```

---

## Step 3: Virtual Environment বানাও (প্রথমবার)

```bash
python -m venv venv
```

---

## Step 4: Virtual Environment Activate করো

**PowerShell:**
```bash
.\venv\Scripts\Activate.ps1
```

**CMD:**
```bash
.\venv\Scripts\activate.bat
```

> যদি PowerShell এ error আসে, তাহলে আগে এটা run করো:
> ```bash
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

## Step 5: Dependencies Install করো (প্রথমবার)

```bash
pip install -r requirements.txt
```

---

## Step 6: Server Run করো 🎉

```bash
python -m uvicorn app.main:app --reload --port 8000
```

---

## Step 7: Browser এ Check করো

- **Health Check:** http://localhost:8000/health
- **API Docs (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Step 8: API Test করো

Swagger Docs (`/docs`) এ গিয়ে:

1. **`GET /health`** তে click করো → "Try it out" → "Execute"
   - Response: `{"status": "ok"}`

2. **`POST /analyze-ticket`** তে click করো → "Try it out" → নিচের JSON paste করো → "Execute"

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

---

## Quick Run (পরের বার থেকে)

শুধু এই 2টা command লাগবে:

```bash
cd "f:\fluuter project\SUST_Preliminary\Backend"
python -m uvicorn app.main:app --reload --port 8000
```

---

## Server বন্ধ করতে

Terminal এ `Ctrl + C` press করো।

---

## ⚠️ Important Notes

- `.env` ফাইলে তোমার real Gemini API key আছে — এটা git এ push করো না
- `.env.example` এ শুধু placeholder আছে, সেটা commit করতে পারো
- `.gitignore` এ `.env` add করা আছে, তাই safe
