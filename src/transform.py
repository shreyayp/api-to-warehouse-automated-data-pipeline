"""Validation and transformation of API response rows."""
import pandas as pd

REQUIRED_COLUMNS = [
    "city", "country", "latitude", "longitude", "forecast_date",
    "fetched_at_utc", "weather_code", "temperature_2m_max",
    "temperature_2m_min", "precipitation_sum",
    "precipitation_probability_max", "wind_speed_10m_max",
]

NUMERIC_COLUMNS = [
    "latitude", "longitude", "weather_code", "temperature_2m_max",
    "temperature_2m_min", "precipitation_sum",
    "precipitation_probability_max", "wind_speed_10m_max",
]

def transform_rows(rows):
    """Convert rows to a typed frame and create derived features."""
    if not rows:
        raise ValueError("No API rows received")

    df = pd.DataFrame(rows)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    df["forecast_date"] = pd.to_datetime(df["forecast_date"], errors="coerce").dt.date.astype("string")
    df["fetched_at_utc"] = pd.to_datetime(df["fetched_at_utc"], errors="coerce", utc=True).astype("string")

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["temperature_range_c"] = df["temperature_2m_max"] - df["temperature_2m_min"]
    df["is_rain_risk"] = df["precipitation_probability_max"].ge(50)
    df["quality_flags"] = ""

    checks = [
        (df["forecast_date"].isna() | df["forecast_date"].eq(""), "invalid_forecast_date"),
        (df["city"].isna() | df["city"].eq(""), "missing_city"),
        (df["temperature_2m_max"].isna(), "missing_max_temperature"),
        (df["temperature_2m_min"].isna(), "missing_min_temperature"),
        (df["precipitation_sum"].isna(), "missing_precipitation"),
        (df["precipitation_probability_max"].lt(0) | df["precipitation_probability_max"].gt(100), "invalid_precipitation_probability"),
        (df["temperature_2m_min"].gt(df["temperature_2m_max"]), "min_temperature_above_max"),
        (df["wind_speed_10m_max"].lt(0), "negative_wind_speed"),
    ]
    for mask, flag in checks:
        mask = mask.fillna(False)
        df.loc[mask, "quality_flags"] = df.loc[mask, "quality_flags"].apply(
            lambda old: f"{old};{flag}" if old else flag
        )

    df["needs_review"] = df["quality_flags"].ne("")
    return df
