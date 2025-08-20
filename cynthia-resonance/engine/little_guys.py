from typing import Dict, Any, List
from .dataset import GATE_META

def _city(name: str) -> List[Dict[str,Any]]:
    out=[]
    for g in range(1,65):
        meta = GATE_META[g]
        out.append({
            "id": f"{name}-{g}",
            "gate": g,
            "city": name,
            "name": meta["name"],
            "element": meta["element"],
            "state": "dormant" if g%4==0 else "unlocked",
            "level": 1 + (g % 3)
        })
    return out

ROSTER = {
    "Mind":  _city("Mind"),
    "Heart": _city("Heart"),
    "Body":  _city("Body"),
}

def roster_dump():
    return ROSTER
