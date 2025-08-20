# Lightweight astro helpers (fallback Sun position by date)
from datetime import datetime, timezone
from .dataset import SIGNS

def sun_longitude_approx(dt_utc: datetime) -> float:
    """
    Very light approximation: map day-of-year to ecliptic longitude.
    Good enough for UX; replace with SharpAstrology for production accuracy.
    """
    year = dt_utc.year
    spring = datetime(year, 3, 20, tzinfo=timezone.utc)  # ~ Aries 0°
    days = (dt_utc - spring).total_seconds() / 86400.0
    lon = (days * (360.0/365.2422)) % 360.0
    return (lon + 360.0) % 360.0

def lon_to_sign_dms(lon: float) -> tuple[str, int, int, int]:
    sign_i = int(lon // 30)
    sign = SIGNS[sign_i]
    deg_total = lon % 30.0
    deg = int(deg_total)
    minutes_f = (deg_total - deg) * 60.0
    minute = int(minutes_f)
    second = int(round((minutes_f - minute) * 60.0))
    if second == 60: second, minute = 0, minute + 1
    if minute == 60: minute, deg = 0, deg + 1
    if deg == 30: deg, sign_i = 0, (sign_i + 1) % 12
    sign = SIGNS[sign_i]
    return sign, deg, minute, second
