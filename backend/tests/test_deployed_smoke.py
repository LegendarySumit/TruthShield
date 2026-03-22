import os

import httpx
import pytest


def test_deployed_smoke_health():
    base_url = os.getenv("DEPLOYED_API_URL", "").strip().rstrip("/")
    if not base_url:
        pytest.skip("DEPLOYED_API_URL is not set")

    response = httpx.get(f"{base_url}/health", timeout=20.0)
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("status") == "alive"
