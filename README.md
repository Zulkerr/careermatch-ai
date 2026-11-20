# CareerMatch AI

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.x-646CFF?logo=vite&logoColor=white)
![CI](https://img.shields.io/badge/GitHub_Actions-CI_Passing-2088FF?logo=githubactions&logoColor=white)

**CareerMatch AI** ist ein KI-gestützter Bewerbungs- und Stellenanzeigen-Analyzer. Die Full-Stack-Anwendung vergleicht einen Lebenslauf mit einer konkreten Stellenanzeige, berechnet einen strukturierten Match-Score, identifiziert übereinstimmende sowie fehlende Skills und generiert konkrete Optimierungsvorschläge inklusive individuellem Anschreiben-Entwurf.

---

## Key Features

- **Automatisierter Match-Score (0–100 %):** Objektive Bewertung der Passung zwischen Kandidatenprofil und Stellenanforderung.
- **Skill-Gap-Analyse:** Strukturierte Trennung in vorhandene (`matched_skills`) und fehlende Kompetenzen (`missing_skills`).
- **Umsetzbare Verbesserungsvorschläge:** Konkrete Empfehlungen zur gezielten Profil- und Lebenslauf-Optimierung.
- **Anschreiben-Generator:** Kontextbezogener Entwurf auf Basis der tatsächlichen Profilstärken.
- **Provider-unabhängige LLM-Architektur:** Anbindung über standardisierte OpenAI-kompatible REST-Schnittstelle (`LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY`) mit strikter Pydantic-Schema-Validierung.

---

## Systemarchitektur

```text
+-----------------------+       HTTP / JSON       +------------------------+
|   React + TypeScript  | ----------------------> |    FastAPI Backend     |
|   (Vite, Port 5174)   | <---------------------- |  (Python, Port 8001)   |
+-----------------------+                         +------------------------+
                                                              |
                                                              | httpx (Async)
                                                              | Pydantic Validation
                                                              v
                                                  +------------------------+
                                                  |  OpenAI-kompatibles    |
                                                  |  LLM-Gateway / API     |
                                                  |  (LLM_BASE_URL /v1)    |
                                                  +------------------------+
```

---

## API-Dokumentation

### `GET /health`
Prüft die Erreichbarkeit des Backends.

**Response (`200 OK`):**
```json
{
  "status": "ok"
}
```

### `POST /api/analyze`
Analysiert Lebenslauf und Stellenanzeige und liefert strukturierte Ergebnisse zurück.

**Request Body:**
```json
{
  "resume_text": "Softwareentwickler mit Erfahrung in Java 17, Spring Boot, Python, FastAPI, React, TypeScript und Docker.",
  "job_description": "Gesucht wird ein Full-Stack Developer (m/w/d) mit Kenntnissen in Java Spring Boot, Python, React, TypeScript, Docker und Kubernetes."
}
```

**Response (`200 OK`):**
```json
{
  "match_score": 83,
  "matched_skills": ["Java", "Spring Boot", "Python", "React", "TypeScript", "Docker"],
  "missing_skills": ["Kubernetes"],
  "suggestions": [
    "Praktische Grundlagen in Kubernetes anhand eines kleinen Demo-Deployments aufbauen",
    "CI/CD- und Container-Erfahrung stärker im Lebenslauf hervorheben"
  ],
  "cover_letter_draft": "Sehr geehrte Damen und Herren, ..."
}
```

---

## Lokale Installation & Start

### Option A: Schnellstart mit Docker Compose (Empfohlen)

```bash
cp .env.example .env
# Trage deinen API-Key in die .env ein
docker compose up --build
```
Anschließend sind Frontend (`http://localhost:5174`) und Backend (`http://localhost:8001/docs`) sofort einsatzbereit.

---

### Option B: Manuelle Installation

### 1. Backend starten (FastAPI)

**Windows (PowerShell):**
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$env:LLM_BASE_URL="http://localhost:3001/v1"
$env:LLM_MODEL="auto"
$env:LLM_API_KEY="dein-api-key"

python main.py
```

**macOS / Linux:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export LLM_BASE_URL="http://localhost:3001/v1"
export LLM_MODEL="auto"
export LLM_API_KEY="dein-api-key"

python main.py
```
Das Backend läuft anschließend unter `http://localhost:8001` (interaktive Swagger-UI unter `http://localhost:8001/docs`).

### 2. Frontend starten (React + Vite)

```bash
cd frontend
npm install
npm run dev
```
Die Weboberfläche ist unter `http://localhost:5174` erreichbar.

---

## Tests & CI/CD

- **Backend-Tests:** Unit- und API-Tests mit `pytest` und gemockten LLM-Antworten (`cd backend && pytest`).
- **Frontend-Build:** TypeScript-Typprüfung und Production-Bundle (`cd frontend && npm run build`).
- **GitHub Actions:** Automatische Ausführung von Backend-Tests und Frontend-Build bei jedem Push auf `main` (`.github/workflows/ci.yml`).
