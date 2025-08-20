# Unified text parser (astro & HD strings) → packet
import re
from typing import Optional, Dict, Any
from .dataset import SIGNS, GATE_META

PERIODIC = {m["element"] for m in GATE_META.values()}

def _int(x:str, lo:int, hi:int) -> Optional[int]:
    try:
        n = int(x)
        return n if lo <= n <= hi else None
    except:
        return None

def parse_astro_text(s: str) -> Dict[str, Any]:
    s = (s or "").strip().replace("deg","°").replace("degrees","°")
    s = re.sub(r"\s+", " ", s)
    # 15° 32' 10" Leo H7   OR   23° Aquarius H11
    d = re.search(r"(\d{1,2})\s*°\s*(\d{1,2})?\s*'?\s*(\d{1,2})?\"?", s)
    sign = None
    for name in SIGNS:
        if re.search(rf"\b{name}\b", s, re.I):
            sign = name; break
    if not sign:
        abbr = {"Ar":"Aries","Ta":"Taurus","Ge":"Gemini","Cn":"Cancer","Le":"Leo","Vi":"Virgo","Li":"Libra","Sc":"Scorpio","Sg":"Sagittarius","Cp":"Capricorn","Aq":"Aquarius","Pi":"Pisces"}
        m = re.search(r"\b(Ar|Ta|Ge|Cn|Le|Vi|Li|Sc|Sg|Cp|Aq|Pi)\b", s, re.I)
        if m: sign = abbr[m.group(1)]
    house = None
    hm = re.search(r"\bH\s*(\d{1,2})\b", s, re.I)
    if hm: house = _int(hm.group(1),1,12)
    deg = int(d.group(1)) if d else None
    minute = int(d.group(2)) if (d and d.group(2)) else None
    second = int(d.group(3)) if (d and d.group(3)) else None
    return {k:v for k,v in dict(sign=sign, degree=deg, minute=minute, second=second, house=house).items() if v is not None}

def parse_hd_text(s: str) -> Dict[str, Any]:
    s = (s or "").strip()
    gate = line = color = tone = base = None
    m = re.search(r"\b(?:gate\s*)?(\d{1,2})\s*\.\s*(\d)\b", s, re.I)
    if m: gate, line = _int(m.group(1),1,64), _int(m.group(2),1,6)
    if gate is None:
        m = re.search(r"\bgate\s*(\d{1,2})\b", s, re.I)
        if m: gate = _int(m.group(1),1,64)
    for tag,key in (("color","color"),("tone","tone"),("base","base")):
        m = re.search(rf"\b{tag}\s*(\d)\b", s, re.I)
        if m:
            val = _int(m.group(1),1,6)
            if key=="color": color=val
            elif key=="tone": tone=val
            else: base=val
    if (m := re.search(r"\bC\s*=?\s*(\d)\b.*?\bT\s*=?\s*(\d)\b.*?\bB\s*=?\s*(\d)\b", s, re.I)):
        color, tone, base = _int(m.group(1),1,6), _int(m.group(2),1,6), _int(m.group(3),1,6)
    return {k:v for k,v in dict(gate=gate,line=line,color=color,tone=tone,base=base).items() if v is not None}

def parse_unified(field: Optional[str], planet: Optional[str], astro_text: Optional[str], hd_text: Optional[str]) -> Dict[str, Any]:
    astro = parse_astro_text(astro_text or "")
    hd = parse_hd_text(hd_text or "")
    gate = hd.get("gate")
    meta = GATE_META.get(gate or -1)
    element = meta.get("element") if meta else None
    return {
        "field": field,
        "planet": planet,
        "astro": astro,
        "hd": hd,
        "meta": {
            "gate_name": meta.get("name") if meta else None,
            "element": element,
            "element_is_real": bool(element and element in PERIODIC),
            "keyword": meta.get("kw") if meta else None
        }
    }
