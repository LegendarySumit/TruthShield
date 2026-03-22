import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Allow importing backend/main.py as module "main"
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import main as app_main  # noqa: E402


client = TestClient(app_main.app)


def test_health_endpoint_returns_runtime_status():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert "status" in payload
    assert "runtime" in payload
    assert "dependencies" in payload


def test_predict_rejects_empty_text():
    response = client.post("/predict", json={"text": "   "})
    assert response.status_code == 400
    payload = response.json()
    assert payload["error"] == "empty_text"


def test_predict_uses_local_fallback_when_gemini_unavailable(monkeypatch):
    monkeypatch.setattr(app_main, "USE_LOCAL_MODEL", True)

    async def _gemini_none(_: str):
        return None

    def _local_ok(_: str):
        return {
            "prediction": "Real",
            "confidence": 0.73,
            "explanation": "fallback",
            "model_version": app_main.MODEL_VERSION,
        }

    monkeypatch.setattr(app_main, "analyze_with_gemini", _gemini_none)
    monkeypatch.setattr(app_main, "analyze_with_local_model", _local_ok)

    text = "This is a long enough article body used for test execution only. "
    response = client.post("/predict", json={"text": text})
    assert response.status_code == 200
    payload = response.json()
    assert payload["prediction"] == "Real"
    assert "model_version" in payload


def test_predict_rate_limit_returns_429(monkeypatch):
    def _blocked(_: str):
        return False, "ip_rate_limit_exceeded", 60

    monkeypatch.setattr(app_main.rate_limiter, "check", _blocked)

    text = "This is a long enough article body used for test execution only. "
    response = client.post("/predict", json={"text": text})
    assert response.status_code == 429
    payload = response.json()
    assert payload["error"] == "ip_rate_limit_exceeded"
