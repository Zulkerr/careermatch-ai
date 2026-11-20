import os
import json
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

app = FastAPI(title="CareerMatch AI Backend")

# CORS-Konfiguration für das Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datenmodelle
class AnalysisRequest(BaseModel):
    resume: str
    job_description: str

class AnalysisResponse(BaseModel):
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    cover_letter_draft: str

# Konfiguration aus Umgebungsvariablen
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:3001/v1").rstrip("/")
LLM_API_KEY = os.getenv("LLM_API_KEY", "no-key-required")
LLM_MODEL = os.getenv("LLM_MODEL", "auto")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    system_prompt = (
        "Du bist ein erfahrener Karriereberater. Analysiere den Lebenslauf gegen die Stellenanzeige. "
        "Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt. "
        "Struktur: { "
        "\"match_score\": Zahl (0-100), "
        "\"matched_skills\": [String], "
        "\"missing_skills\": [String], "
        "\"suggestions\": [String], "
        "\"cover_letter_draft\": \"String\" "
        "}"
    )
    user_prompt = f"LEBENSLAUF:\n{request.resume}\n\nSTELLENANZEIGE:\n{request.job_description}"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{LLM_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {LLM_API_KEY}"},
                json={
                    "model": LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"}
                }
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"LLM API Error: {response.text}"
                )

            llm_data = response.json()
            content = llm_data["choices"][0]["message"]["content"]

            # Parsen des JSON-Strings aus der LLM-Antwort
            parsed_result = json.loads(content)

            return AnalysisResponse(**parsed_result)

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="LLM lieferte kein gültiges JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
