# tests/test_grader.py
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_grade():
    response = client.post(
        "/grade",
        json={
            "essay": "This is a sample essay...",
            "rubric": {
                "Accuracy": {"3": "Excellent", "2": "Good", "1": "Needs work"},
                "Mechanics": {"3": "Perfect", "2": "Some errors", "1": "Poor"},
            },
            "slo_choice": "Critical thinking",
        },
        headers={"X-API-Key": "my_secret_key_123"},
    )
    assert response.status_code == 200
    assert "scores" in response.json()
