import pytest
from fastapi.testclient import TestClient
from main import app
import json
from unittest.mock import AsyncMock, patch, MagicMock

client = TestClient(app)

def test_health():
    """Testet den Health-Check Endpunkt."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_analyze_success(mock_post):
    """Testet den Analyse-Endpunkt mit einer erfolgreichen gemockten LLM-Antwort."""
    # Mock der LLM-Antwort
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "match_score": 85,
                    "matched_skills": ["Python", "FastAPI", "REST-API"],
                    "missing_skills": ["React", "TypeScript"],
                    "suggestions": ["Lerne die Grundlagen von React.", "Erstelle ein TypeScript-Portfolio."],
                    "cover_letter_draft": "Sehr geehrte Damen und Herren, als erfahrener Python-Entwickler..."
                })
            }
        }]
    }
    mock_post.return_value = mock_response

    # Test-Daten
    payload = {
        "resume": "Ich bin ein Python-Entwickler mit Erfahrung in FastAPI.",
        "job_description": "Wir suchen einen Fullstack-Entwickler mit Python und React."
    }

    response = client.post("/api/analyze", json=payload)

    # Validierung
    if response.status_code != 200:
        print(f"Error detail: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert data["match_score"] == 85
    assert "Python" in data["matched_skills"]
    assert "React" in data["missing_skills"]
    assert "suggestions" in data
    assert "cover_letter_draft" in data
    assert len(data["suggestions"]) == 2

@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
def test_analyze_error(mock_post):
    """Testet das Verhalten bei einem API-Fehler des LLM."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response

    payload = {
        "resume": "...",
        "job_description": "..."
    }

    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 500
    assert "LLM API Error" in response.json()["detail"]
