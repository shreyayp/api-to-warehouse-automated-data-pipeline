"""SQLite loading and report generation."""
import json
import sqlite3
from datetime import datetime, timezone
import pandas as pd
from config import DB_PATH, CSV_PATH, PROCESSED_DIR, REPORTS_DIR

def load_to_sqlite(df, run_metadata, quality_report):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Forecast snapshots are retained by fetched_at_utc, so repeated runs
    # can be compared rather than silently overwriting earlier forecasts.
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("weather_forecast", conn, if_exists="append", index=False)
        pd.DataFrame(run_metadata).to_sql("pipeline_runs", conn, if_exists="append", index=False)
        quality_db = quality_report.copy()
        quality_db["errors"] = json.dumps(quality_report.get("errors", []))
        pd.DataFrame([quality_db]).to_sql("quality_checks", conn, if_exists="append", index=False)

        summary = pd.read_sql_query("""
            SELECT city,
                   COUNT(*) AS forecast_rows,
                   ROUND(AVG(temperature_2m_max), 1) AS avg_max_temp_c,
                   ROUND(MAX(temperature_2m_max), 1) AS highest_max_temp_c,
                   ROUND(SUM(precipitation_sum), 1) AS total_forecast_precip_mm,
                   ROUND(MAX(precipitation_probability_max), 0) AS highest_precip_probability_pct,
                   ROUND(MAX(wind_speed_10m_max), 1) AS max_wind_speed_kmh
            FROM weather_forecast
            WHERE fetched_at_utc = (SELECT MAX(fetched_at_utc) FROM weather_forecast)
            GROUP BY city
            ORDER BY avg_max_temp_c DESC
        """, conn)
        summary.to_csv(REPORTS_DIR / "city_forecast_summary.csv", index=False)

        rain_risk = pd.read_sql_query("""
            SELECT city, forecast_date, temperature_2m_max, precipitation_sum,
                   precipitation_probability_max, wind_speed_10m_max
            FROM weather_forecast
            WHERE fetched_at_utc = (SELECT MAX(fetched_at_utc) FROM weather_forecast)
              AND precipitation_probability_max >= 50
            ORDER BY precipitation_probability_max DESC, city, forecast_date
        """, conn)
        rain_risk.to_csv(REPORTS_DIR / "rain_risk_days.csv", index=False)

    df.to_csv(CSV_PATH, index=False)
    (REPORTS_DIR / "data_quality_report.json").write_text(
        json.dumps(quality_report, indent=2), encoding="utf-8"
    )
    (REPORTS_DIR / "latest_run.json").write_text(
        json.dumps(run_metadata, indent=2), encoding="utf-8"
    )
