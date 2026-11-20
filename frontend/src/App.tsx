import { useState } from 'react'
import './App.css'

interface AnalysisResponse {
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  suggestions: string[];
  cover_letter_draft: string;
}

function App() {
  const [resume, setResume] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!resume || !jobDescription) {
      alert('Bitte fülle beide Felder aus.');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8001/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ resume, job_description: jobDescription }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Fehler bei der Analyse');
      }

      const data: AnalysisResponse = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Ein unerwarteter Fehler ist aufgetreten.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>CareerMatch AI</h1>
        <p>Optimiere deine Bewerbung mit KI-Unterstützung</p>
      </header>

      <main>
        <div className="input-section">
          <div className="field">
            <label htmlFor="resume">Dein Lebenslauf / Profil</label>
            <textarea
              id="resume"
              placeholder="Füge hier deinen Lebenslauf oder dein Profil ein..."
              value={resume}
              onChange={(e) => setResume(e.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="jobDescription">Stellenanzeige</label>
            <textarea
              id="jobDescription"
              placeholder="Füge hier die Stellenanzeige ein..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>
        </div>

        <div className="action-bar">
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className={loading ? 'loading' : ''}
          >
            {loading ? 'Analysiere...' : 'Jetzt analysieren'}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {result && (
          <div className="result-section">
            <div className="score-card">
              <h3>Match Score</h3>
              <div className="score-circle">
                <span>{result.match_score}%</span>
              </div>
            </div>

            <div className="details-grid">
              <div className="detail-box">
                <h4>Gefundene Skills</h4>
                <ul>
                  {result.matched_skills.map((skill, i) => (
                    <li key={i} className="skill-tag matched">{skill}</li>
                  ))}
                </ul>
              </div>
              <div className="detail-box">
                <h4>Fehlende Skills</h4>
                <ul>
                  {result.missing_skills.map((skill, i) => (
                    <li key={i} className="skill-tag missing">{skill}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="suggestions-box">
              <h4>Verbesserungsvorschläge</h4>
              <ul>
                {result.suggestions.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>

            <div className="cover-letter-box">
              <h4>Anschreiben Entwurf</h4>
              <pre>{result.cover_letter_draft}</pre>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
