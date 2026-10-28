"""API ingestion functions."""
from datetime import datetime, timezone
import requests
from config import API_URL, FORECAST_DAYS

DAILY_FIELDS = [
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "precipitation_probability_max",
    "wind_speed_10m_max",
]

def fetch_city_forecast(city, session=None):
    """Fetch daily forecast JSON for one configured city."""
    client = session or requests.Session()
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "daily": ",".join(DAILY_FIELDS),
        "forecast_days": FORECAST_DAYS,
        "timezone": "Asia/Kolkata",
    }
    response = client.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if payload.get("error"):
        raise ValueError(f"API returned an error for {city['city']}: {payload.get('reason')}")

    daily = payload.get("daily")
    if not isinstance(daily, dict) or "time" not in daily:
        raise ValueError(f"API response for {city['city']} did not include daily forecast data")

    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = []
    for i, forecast_date in enumerate(daily["time"]):
        row = {
            "city": city["city"],
            "country": city["country"],
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "forecast_date": forecast_date,
            "fetched_at_utc": fetched_at,
        }
        for field in DAILY_FIELDS:
            values = daily.get(field, [])
            row[field] = values[i] if i < len(values) else None
        rows.append(row)

    return rows, {
        "city": city["city"],
        "fetched_at_utc": fetched_at,
        "api_timezone": payload.get("timezone"),
        "api_elevation_m": payload.get("elevation"),
        "row_count": len(rows),
    }
