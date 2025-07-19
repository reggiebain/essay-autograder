import os
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

@pytest.mark.skipif(
    os.getenv("ENABLE_LIVE_API_TESTS", "false").lower() != "true",
    reason="Skipping test to avoid using OpenAI tokens during CI"
)
def test_grade():
    test_api_key = os.getenv("API_KEY", "dummy_key")

    response = client.post("/grade", json={
        "essay": "This is a sample essay about climate change...",
        "rubric": {
            "Accuracy": {"3": "Excellent", "2": "Good", "1": "Needs work"},
            "Mechanics": {"3": "Perfect", "2": "Some errors", "1": "Poor"}
        }
    }, headers={"X-API-Key": test_api_key})

    assert response.status_code == 200
    assert "scores" in response.json()
    assert "feedback" in response.json()
