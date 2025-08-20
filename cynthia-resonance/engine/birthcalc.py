from dataclasses import dataclass
from datetime import datetime, timezone
from dateutil import tz
from typing import Optional, Tuple, Dict, Any
from .astro import sun_longitude_approx, lon_to_sign_dms
from .hd import sun_to_gate_line
from .dataset import GATE_META

@dataclass
class Birth:
    dateISO: str
    time: Optional[str] = None      # "HH:MM" (24h)
    tzOffset: Optional[float] = None# hours, e.g. -4 for EDT
    lat: Optional[float] = None
    lon: Optional[float] = None

def _dt_utc(b: Birth) -> datetime:
    # Best effort: date + time + tzOffset → UTC
    date_str = b.dateISO.strip()
    time_str = (b.time or "12:00").strip()
    hh, mm = [int(x) for x in time_str.split(":")]
    if b.tzOffset is not None:
        tzinfo = tz.tzoffset(None, int(b.tzOffset * 3600))
    else:
        tzinfo = timezone.utc
    local_dt = datetime.fromisoformat(f"{date_str}T{hh:02d}:{mm:02d}:00").replace(tzinfo=tzinfo)
    return local_dt.astimezone(timezone.utc)

def _today_utc(dateISO: Optional[str] = None) -> datetime:
    return (datetime.fromisoformat(dateISO).replace(tzinfo=timezone.utc)
            if dateISO else datetime.now(timezone.utc))

def calc_birth(b: Birth) -> Tuple[Dict[str,Any], Dict[str,Any], Dict[str,Any]]:
    """
    Returns (astro, hd, auric) for the natal Sun, minutes/seconds included.
    Fallback model; replace later with SharpAstrology + HDKit adapters if desired.
    """
    dt_utc = _dt_utc(b)
    ecl = sun_longitude_approx(dt_utc)
    sign, deg, minute, second = lon_to_sign_dms(ecl)
    astro = {"placements":[{"planet":"Sun","sign":sign,"degree":deg,"minute":minute,"second":second,"house":None}]}
    gate, line = sun_to_gate_line(ecl)
    hd = {"sun":{"gate":gate,"line":line}}
    meta = GATE_META.get(gate, {})
    auric = {
        "archetype":{
            "gate":gate,"line":line,"name":meta.get("name"),
            "element":meta.get("element")
        },
        "utility":{
            "plane":"Body","stance":"personal","expression":"action"
        },
        "resonance":{
            "sign":sign,"deg":deg,"min":minute,"sec":second,"house":None,
            "axis": f"{gate} ↔ {(gate+32-1)%64+1}",
            "field_weights":{"mind":0.33,"heart":0.33,"body":0.34}
        },
        "coherence":{"score":9,"mode":"Prime","sparkle":False}
    }
    return astro, hd, auric
