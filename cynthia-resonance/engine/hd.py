# Fallback HD: map ecliptic longitude → gate/line deterministically
def sun_to_gate_line(ecl_lon_deg: float) -> tuple[int, int]:
    # 360 / 64 = 5.625° per gate; 6 lines per gate → 0.9375° per line
    gate = max(1, min(64, int(ecl_lon_deg / 5.625) + 1))
    within = ecl_lon_deg % 5.625
    line = max(1, min(6, int(within / (5.625/6.0)) + 1))
    return gate, line
