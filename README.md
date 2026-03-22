# 🛡️ TruthShield - AI-Powered Fake News Detector

![TruthShield](https://img.shields.io/badge/Predictions-Probabilistic-orange)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![React](https://img.shields.io/badge/React-19-61dafb)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

**Unmask the Truth with AI** - Detect potentially misleading news quickly using advanced Machine Learning and Natural Language Processing.

---

## 🚀 Quick Start

```bash
# 1. Start Backend (Terminal 1)
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# 2. Start Frontend (Terminal 2)
cd frontend
npm run dev

# 3. Open Browser
http://localhost:5173
```

---

## ✨ Features

- ⚡ **Lightning Fast** - Results in <1 second
- 🎯 **Probabilistic Scoring** - Confidence-based output, not absolute certainty
- 🎨 **Beautiful UI** - Glassmorphism design with smooth animations
- 🔒 **Privacy First** - Zero data collection or tracking
- 🧭 **Versioned API** - Stable `/api/v1` contract with legacy route compatibility
- 🛡️ **Abuse Protection** - Rate-limiting plus optional Turnstile captcha
- 🧪 **CI Browser E2E** - Playwright prediction-flow gate with safe captcha bypass in CI
- 📱 **Responsive** - Works on all devices
- 🌙 **Dark Mode** - Easy on the eyes
- 📚 **Educational** - Learn how fake news detection works

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Validation Approach** | Held-out evaluation + live model monitoring |
| **Output Type** | Probabilistic classification with confidence score |
| **Training Samples** | 640 articles |
| **Test Samples** | 160 articles |
| **Features Extracted** | 1,360 linguistic markers |
| **Prediction Speed** | <100ms |

---

## ⚠️ Model Limitations and Responsible Use

- TruthShield predictions can produce false positives and false negatives.
- Confidence scores indicate model certainty, not factual proof.
- Outputs should be treated as decision support, not final truth.
- Always verify important claims with independent, authoritative sources.

---

## ✅ Acceptable Use

- Use TruthShield for research, education, and editorial triage.
- Do not use it as the sole basis for legal, medical, financial, or safety-critical decisions.
- Do not submit illegal, abusive, or harmful content.
- Do not misrepresent TruthShield output as guaranteed fact.

---

## 🧭 P1 Operational Readiness

### Observability

- Structured JSON logging with request and trace IDs.
- `/metrics` endpoint for Prometheus scraping (request count, latency, 5xx, fallback counters).
- Optional Sentry integration via `SENTRY_DSN`.
- Built-in threshold alerts in logs for high latency and elevated 5xx rates.

### Gemini Resilience

- Configurable timeout/retries/jitter (`GEMINI_*` env vars).
- Circuit breaker on repeated Gemini failures.
- Explicit Gemini success and local fallback metrics.
- Bounded TTL cache for repeated requests.

### Model Lifecycle

- Versioned response field `model_version`.
- Training now emits:
    - `backend/models/model_metadata.json`
    - `backend/models/evaluation_report.json`
- Startup integrity checks validate model/vectorizer interface compatibility and runtime/training version alignment.

### Drift Monitoring Plan

1. Capture weekly aggregate prediction distributions and confidence buckets.
2. Compare with baseline ranges from the last stable evaluation report.
3. Trigger retraining if drift exceeds threshold for 2 consecutive windows.
4. Re-run training and publish updated metadata/evaluation artifacts.
5. Promote only after staging smoke checks pass.

### API Versioning and Contract Policy

- Preferred stable API namespace is `/api/v1`.
- Legacy unversioned routes remain available for backward compatibility.
- Compatibility policy endpoint: `/api/v1/version-policy`.
- OpenAPI schemas include curated examples for request/response models.

### Data and Privacy Governance

- Default submitted-text retention is `0` days (no request body persistence).
- Optional privacy-first mode: set `NO_STORE_MODE=true` to disable API cache and enforce `Cache-Control: no-store` headers.
- Governance details are exposed via `/api/v1/health` under `data_governance`.

### Business Continuity

- Incident response, backup/rollback strategy, and post-deploy verification are defined in [docs/operations-runbook.md](docs/operations-runbook.md).
- CI includes browser E2E prediction-flow validation using Playwright with staging test-mode captcha bypass.

---

## 🏗️ Project Structure

```
TruthShield/
├── backend/
│   ├── main.py                    # FastAPI app and API endpoints
│   ├── train_v3.py                # Model training script (v3)
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_deployed_smoke.py
│   ├── models/                    # model.pkl, vectorizer.pkl, metadata
│   └── Enhanced_Dataset_v3.csv    # Training data
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── test/
│   │   └── lib/
│   └── .env.example
├── docs/
│   └── operations-runbook.md
├── docker-compose.yml
└── render.yaml
```

## Local Development Setup

### 1. Prerequisites

- Python 3.8+
- Node.js 14+
- Docker (optional, for containerized setup)

### 2. Backend Setup

**Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

**Install Python dependencies:**

```bash
pip install -r backend/requirements.txt
```

**Train the ML model:**

The repository already includes `Enhanced_Dataset_v3.csv` for training.
If you want larger/alternative data, you can also add `Fake.csv` and `True.csv` from Kaggle: [https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)

Then, run the training script:

```bash
python backend/train_v3.py
```

This will create `model.pkl` and `vectorizer.pkl` in the `backend/models/` directory.

**Run the backend server:**

```bash
uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 3. Frontend Setup

**Navigate to the frontend directory and install dependencies:**

```bash
cd frontend
npm install
cp .env.example .env  # On Windows PowerShell: Copy-Item .env.example .env
```

**Run the frontend development server:**

```bash
npm run dev
```

The application will be available at `http://localhost:5173` (or another port if 5173 is busy).

## Docker Setup

With Docker installed, you can run the entire application with a single command:

```bash
docker-compose up --build
```

The frontend will be available at `http://localhost:3000` and the backend at `http://localhost:8000`.

## Deployment

The application is designed to be easily deployable on platforms like Vercel (for the frontend) and Render (for the backend).

### Vercel (Frontend)

1.  Connect your Git repository to Vercel.
2.  Set the framework to "Vite".
3.  Add environment variables:
    - `VITE_API_URL` = your deployed backend base URL
    - `VITE_REQUEST_TIMEOUT_MS` = `12000`
    - `VITE_CAPTCHA_BYPASS` = `false` (keep disabled in production)
    - `VITE_ANALYTICS_ENABLED` = `false` unless you have a telemetry endpoint
4.  Deploy!

### Render (Backend)

1.  Connect your Git repository to Render.
2.  Create a new Web Service.
3.  Set the runtime to "Python 3".
4.  Set the build command to `pip install -r requirements.txt`.
5.  Set the start command to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
6.  Configure required production environment variables:
    - `ENVIRONMENT=production`
    - `FORCE_HTTPS=true`
    - `TRUSTED_HOSTS=<your-render-domain>`
    - `CORS_ALLOW_ORIGINS=<your-frontend-domain>`
    - `CORS_DEV_ALLOW_ALL=false`
    - `GEMINI_API_KEY=<secret>`
    - `NO_STORE_MODE=true`
    - `RETENTION_DAYS_SUBMITTED_TEXT=0`
    - `PRIVACY_CONTACT_EMAIL=privacy@truthshield.ai`
    - If captcha is enabled: `CAPTCHA_ENABLED=true`, `CAPTCHA_SECRET_KEY=<secret>`
7.  Deploy!

