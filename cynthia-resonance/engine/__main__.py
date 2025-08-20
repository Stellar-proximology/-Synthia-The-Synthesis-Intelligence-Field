# Handy CLI for quick checks
import json, sys
from .birthcalc import Birth, calc_birth
from .interference import calc_interference, plan_from_interference

if __name__ == "__main__":
    b = Birth(dateISO=sys.argv[1], time=sys.argv[2] if len(sys.argv)>2 else "12:00", tzOffset=float(sys.argv[3]) if len(sys.argv)>3 else 0)
    astro, hd, auric = calc_birth(b)
    inter = calc_interference(astro, hd, auric, None)
    plan = plan_from_interference(inter, auric)
    print(json.dumps({"astro":astro,"hd":hd,"plan":plan}, indent=2))
