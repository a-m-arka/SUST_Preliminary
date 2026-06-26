# QueueStorm Investigator API

AI-powered customer support ticket analysis service built with **FastAPI** and **Google Gemini** for the SUST Preliminary Hackathon.

## 🚀 Live Demo

**API Base URL:**
https://sustpreliminary-production-baaa.up.railway.app/

**Interactive API Documentation (Swagger):**
https://sustpreliminary-production-baaa.up.railway.app/docs

**Health Check:**
https://sustpreliminary-production-baaa.up.railway.app/health

---

## 📌 Overview

QueueStorm Investigator is an intelligent backend service that analyzes customer support tickets related to digital financial services.

Given a customer's complaint and transaction history, the API automatically:

* Identifies the most relevant transaction
* Determines whether the complaint matches available evidence
* Classifies the case type
* Assesses severity
* Routes the ticket to the appropriate department
* Generates an internal summary for support agents
* Drafts a professional customer response
* Determines whether human review is required

---

## ✨ Features

* 🤖 AI-powered ticket analysis using Google Gemini
* ⚡ FastAPI REST API
* 📄 Automatic Swagger/OpenAPI documentation
* 🔒 Safety validation for AI-generated responses
* 🧠 Evidence-based transaction matching
* 🌐 Railway deployment
* ✅ Health monitoring endpoint

---

## 🛠 Tech Stack

* Python 3.11+
* FastAPI
* Google Gemini API
* Pydantic
* Uvicorn
* Railway

---

## 📁 Project Structure

```
app/
│
├── core/
│   └── config.py
│
├── routes/
│   ├── analyze.py
│   └── health.py
│
├── schemas/
│   ├── request.py
│   ├── response.py
│   ├── transaction.py
│   └── gemini_response.py
│
├── services/
│   ├── gemini.py
│   └── prompt.py
│
├── utils/
│   └── safety.py
│
└── main.py
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-2.5-flash
```

---

## ▶️ Run Locally

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### Health Check

```
GET /health
```

Response

```json
{
  "status": "ok"
}
```

---

### Analyze Ticket

```
POST /analyze-ticket
```

Example Request

```json
{
  "ticket_id": "TKT-001",
  "complaint": "I accidentally transferred 5000 taka to the wrong number.",
  "language": "en",
  "channel": "in_app_chat",
  "user_type": "customer",
  "campaign_context": null,
  "transaction_history": [],
  "metadata": {}
}
```

---

## 🧪 Testing

You can test the API using:

* Swagger UI
* Postman
* Insomnia
* cURL

---

## 🚀 Deployment

The application is deployed on **Railway**.

Production URL:

https://sustpreliminary-production-baaa.up.railway.app/

---

## 👨‍💻 Author

Developed for the **SUST Preliminary Hackathon**.

---

## 📄 License

This project was developed solely for the hackathon evaluation and educational purposes.
