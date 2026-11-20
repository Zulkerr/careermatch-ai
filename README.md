# CareerMatch AI

KI-gestützter Bewerbungs- und Stellenanzeigen-Analyzer.

## Architektur
- **Backend**: Python 3.12, FastAPI, Pydantic, Httpx.
- **Frontend**: React, TypeScript, Vite.
- **LLM**: Unterstützt OpenAI-kompatible APIs (konfigurierbar via `LLM_BASE_URL` und `LLM_MODEL`).

## Startanleitung

### Backend
```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate # Windows
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
