import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from engine.birthcalc import Birth, calc_birth
from engine.interference import calc_interference, plan_from_interference
from engine.adapters import maybe_narrate
from engine.parsers import parse_unified
from engine.little_guys import roster_dump

PORT = int(os.getenv("PORT", "8787"))
app = FastAPI(title="Cynthia Resonance", version="0.1.0")

# ----- Schemas -----
class BirthIn(BaseModel):
    dateISO: str
    time: str | None = None
    tzOffset: float | None = None
    lat: float | None = None
    lon: float | None = None

class InterfIn(BirthIn):
    dateTodayISO: str | None = None   # if you want a different transit date than "now"

class PlanIn(InterfIn):
    narrate: bool = False
    mode: str | None = None           # Venom / Echo / Prime / Dream / Softcore (affects style for narration)

class ParseIn(BaseModel):
    field: str | None = None          # "Mind"|"Heart"|"Body"
    planet: str | None = None
    astro: str | None = None          # e.g. "15° 32' Leo H7"
    hd: str | None = None             # e.g. "Gate 6.3, Color 4 Tone 2 Base 6"

# ----- Endpoints -----
@app.get("/health")
def health():
    return {
        "ok": True,
        "ollama": os.getenv("OLLAMA_BASE", None),
        "models": {
            "coach": os.getenv("COACH_MODEL","phi"),
            "mind":  os.getenv("MIND_MODEL","mistral"),
            "heart": os.getenv("HEART_MODEL","tinyllama"),
            "body":  os.getenv("BODY_MODEL","tinyllama"),
        }
    }

@app.post("/api/birth")
def api_birth(inp: BirthIn):
    astro, hd, auric = calc_birth(Birth(**inp.model_dump()))
    return {"astro": astro, "hd": hd, "auric": auric}

@app.post("/api/interference")
def api_interf(inp: InterfIn):
    astro, hd, auric = calc_birth(Birth(**inp.model_dump()))
    inter = calc_interference(astro, hd, auric, inp.dateTodayISO)
    return inter

@app.post("/api/plan")
def api_plan(inp: PlanIn):
    astro, hd, auric = calc_birth(Birth(**inp.model_dump()))
    inter = calc_interference(astro, hd, auric, inp.dateTodayISO)
    plan = plan_from_interference(inter, auric)
    out = {"plan": plan, "astro": astro, "hd": hd, "auric": auric}
    if inp.narrate:
        out["narration"] = maybe_narrate(plan, mode=inp.mode or "Prime")
    return out

@app.get("/api/agents")
def api_agents():
    return roster_dump()

@app.post("/api/parse")
def api_parse(inp: ParseIn):
    return parse_unified(field=inp.field, planet=inp.planet, astro_text=inp.astro, hd_text=inp.hd)
