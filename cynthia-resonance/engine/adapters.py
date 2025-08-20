# Optional external adapters + Ollama narrator
import os, json, re, httpx

OLLAMA = os.getenv("OLLAMA_BASE")
COACH_MODEL = os.getenv("COACH_MODEL","phi")

JSON_RE = re.compile(r"\{.*\}", re.S)

def _ollama_generate(model: str, prompt: str, timeout: float = 60.0) -> str:
    if not OLLAMA:
        return ""
    url = f"{OLLAMA}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    with httpx.Client(timeout=timeout) as c:
        r = c.post(url, json=payload)
        r.raise_for_status()
        return r.json().get("response","").strip()

def maybe_narrate(plan: dict, mode: str = "Prime") -> dict:
    """
    Optional: turn plan JSON into a short coaching note.
    Returns { text, model } or {} if Ollama not set.
    """
    if not OLLAMA:
        return {}
    style = {
        "Venom":"Cut the fluff. Be sharp, honest, brief.",
        "Prime":"Action-forward, concrete step, confident.",
        "Echo":"Reflective, gentle mirroring, validate first.",
        "Dream":"Poetic, metaphor, possibility tone.",
        "Softcore":"Warm, friendly, low pressure."
    }.get(mode,"Prime")
    sys = f"You are Cynthia, a resonance coach. Style: {style}. Reply ONLY as JSON: {{\"text\":\"...\"}}."
    user = f"PLAN_JSON:\n{json.dumps(plan, ensure_ascii=False)}"
    raw = _ollama_generate(COACH_MODEL, sys + "\n\n" + user)
    if not raw:
        return {}
    try:
        m = JSON_RE.search(raw) or re.search(r".*", raw)
        obj = json.loads(m.group(0)) if m else {"text": raw}
        return {"text": obj.get("text", raw).strip(), "model": COACH_MODEL}
    except Exception:
        return {"text": raw, "model": COACH_MODEL}
