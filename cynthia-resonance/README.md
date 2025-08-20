# Cynthia Resonance – Natal → Interference → Plan (with optional AI narration)

## What this is
- Core engine that turns **birth date/time/place** into a **daily resonance plan**:
  1) Natal Sun position (fallback calc) and HD gate/line (fallback map)
  2) Simple daily transit (Sun today) + aspects vs natal
  3) Interference scores for **Mind / Heart / Body**
  4) A structured **/plan** JSON you can feed to a UI or to an AI narrator
- Optional: calls **Ollama** locally to narrate the plan (Phi/TinyLlama/Mistral).

> You can later swap the fallbacks for **SharpAstrology** and **HDKit** by wiring their adapters in `engine/adapters.py`.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # edit if needed

# (Optional) pull local models
# ollama pull phi && ollama pull tinyllama && ollama pull mistral

uvicorn server:app --reload --port 8787

Test

curl -s -X POST http://localhost:8787/api/birth \
  -H 'content-type: application/json' \
  -d '{"dateISO":"1994-07-01","time":"08:25","tzOffset":-4,"lat":40.7128,"lon":-74.0060}' | jq

curl -s -X POST http://localhost:8787/api/plan \
  -H 'content-type: application/json' \
  -d '{"dateISO":"1994-07-01","time":"08:25","tzOffset":-4,"lat":40.7128,"lon":-74.0060,"narrate":true}' | jq

Endpoints

POST /api/birth → { astro, hd, auric }

POST /api/interference → { triad, aspects, interference_index }

POST /api/plan → { plan, (optional) narration }

GET  /api/agents → roster of 3 × 64 “little guys” with states

POST /api/parse → unified text parser (astro/HD strings → packet)


Swap in real engines later

Add your SharpAstrology HTTP microservice → set SharpAstrologyAdapter in engine/adapters.py

Add your HDKit microservice or in‑proc call → set HDKitAdapter similarly
