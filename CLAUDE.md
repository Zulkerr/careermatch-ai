# CareerMatch AI - Architektur & Leitfaden

## Projektziel
KI-gestützter Bewerbungs- und Stellenanzeigen-Analyzer.

## Architektur & Services
- **Backend (/backend)**: Python 3.12 + FastAPI (Port 8001), httpx, pydantic.
  - Endpoint POST /api/analyze nimmt { "resume": "...", "job_description": "..." } entgegen.
  - Sendet Anfrage an OpenAI-kompatible LLM-API (LLM_BASE_URL Standard: http://localhost:3001/v1, LLM_API_KEY).
  - Gibt strukturiertes JSON zurück: match_score (0-100), matched_skills (Liste), missing_skills (Liste), suggestions (Liste), cover_letter_draft (String).
  - Endpoint GET /health und CORS für http://localhost:5174.
- **Frontend (/frontend)**: React + TypeScript + Vite (Port 5174).
  - Zwei Textfelder (Lebenslauf/Profil & Stellenanzeige), Analyse-Button und visuelle Auswertung.
- **Testing**: pytest im Ordner /backend mit gemockten LLM-Antworten.
