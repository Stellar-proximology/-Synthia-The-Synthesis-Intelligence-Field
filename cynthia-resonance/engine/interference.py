from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import math
from .astro import sun_longitude_approx, lon_to_sign_dms
from .hd import sun_to_gate_line
from .dataset import GATE_META

def _today(dt_iso: Optional[str]) -> datetime:
    return datetime.fromisoformat(dt_iso).replace(tzinfo=timezone.utc) if dt_iso else datetime.now(timezone.utc)

def _aspect_score(delta_deg: float) -> float:
    """Return -1..+1: how harmonious is the angle (0=conj, 60=sextile, 120=trine, 90=square, 180=opp)."""
    d = abs((delta_deg + 180) % 360 - 180)  # 0..180
    # simple bumps at 0/60/120 (positive) and dips at 90/180 (negative)
    harm = (
        math.exp(- (d/20)**2 )      * 1.0 +   # conj wide bump
        math.exp(- ((d-60)/12)**2 ) * 0.6 +
        math.exp(- ((d-120)/12)**2) * 0.6 -
        math.exp(- ((d-90)/10)**2 ) * 0.8 -
        math.exp(- ((d-180)/10)**2) * 0.5
    )
    # squash to -1..+1
    return max(-1.0, min(1.0, harm))

def _triad_weights(harm: float) -> Dict[str, float]:
    """
    Turn harmony (-1..+1) into Mind/Heart/Body weights.
    Idea: harmony boosts Heart & Body (flow, action),
          dissonance boosts Mind (analysis).
    """
    heart = max(0.05, 0.5 + 0.4*harm)
    body  = max(0.05, 0.35 + 0.3*harm)
    mind  = max(0.05, 0.45 - 0.6*harm)
    s = heart + body + mind
    return {
        "Mind":  round(mind/s,3),
        "Heart": round(heart/s,3),
        "Body":  round(body/s,3)
    }

def calc_interference(astro: Dict[str,Any], hd: Dict[str,Any], auric: Dict[str,Any], date_today_iso: Optional[str]) -> Dict[str,Any]:
    natal = astro["placements"][0]
    # natal Sun longitude from sign + deg
    sign_index = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"].index(natal["sign"])
    natal_lon = sign_index*30 + natal["degree"] + (natal.get("minute",0)/60.0) + (natal.get("second",0)/3600.0)

    now = _today(date_today_iso)
    trans_lon = sun_longitude_approx(now)
    delta = (trans_lon - natal_lon + 360.0) % 360.0
    harm = _aspect_score(delta)
    weights = _triad_weights(harm)

    sign, deg, minute, second = lon_to_sign_dms(trans_lon)
    t_gate, t_line = sun_to_gate_line(trans_lon)

    aspects = {
        "natal_sun_lon": round(natal_lon,3),
        "transit_sun_lon": round(trans_lon,3),
        "delta_deg": round(((delta+180)%360)-180,3),
        "harmony": round(harm,3),
        "transit": {"sign":sign,"deg":deg,"min":minute,"sec":second,"gate":t_gate,"line":t_line}
    }

    idx = round((weights["Heart"]*1.2 + weights["Body"]*1.0 + weights["Mind"]*0.8),3)
    return {
        "triad": weights,
        "aspects": aspects,
        "interference_index": idx
    }

def plan_from_interference(inter: Dict[str,Any], auric: Dict[str,Any]) -> Dict[str,Any]:
    """
    Deterministic coaching skeleton (works without LLM).
    """
    w = inter["triad"]; harm = inter["aspects"]["harmony"]
    gate = auric["archetype"]["gate"]; meta = GATE_META.get(gate, {})
    head = f"Gate {gate} · {meta.get('name','Gate')}"
    theme = meta.get("kw","pattern")
    # Pick a tone
    if harm >= 0.6:
        tone = "high_flow"
        tip = "Lean into momentum. Share and ship."
    elif harm >= 0.2:
        tone = "flow"
        tip = "Good window for steady progress."
    elif harm >= -0.2:
        tone = "neutral"
        tip = "Tidy the edges, prep the runway."
    elif harm >= -0.6:
        tone = "friction"
        tip = "De-risk choices and move small."
    else:
        tone = "high_friction"
        tip = "Pause big moves. Work on foundations."

    # Triad suggestion
    leader = max(w, key=lambda k: w[k])
    by_lead = {
        "Mind":  "Make a one‑page plan and decompose to first two steps.",
        "Heart": "Have the talk; name your feeling and invite one voice.",
        "Body":  "Do the smallest embodied action in 5–10 minutes."
    }[leader]

    return {
        "headline": head,
        "theme": theme,
        "tone": tone,
        "triad_weights": w,
        "interference_index": inter["interference_index"],
        "today": inter["aspects"]["transit"],
        "suggestions": [
            tip,
            by_lead,
            "Log outcome tonight (win/learn) to tune tomorrow."
        ]
    }
