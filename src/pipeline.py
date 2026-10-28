"""Orchestrate extraction, transformation, quality checks, and loading."""
from datetime import datetime, timezone
import json
import sys
from config import CITIES, REPORTS_DIR
from src.extract import fetch_city_forecast
from src.transform import transform_rows
from src.load import load_to_sqlite

def main():
    all_rows = []
    city_runs = []
    errors = []

    for city in CITIES:
        try:
            rows, metadata = fetch_city_forecast(city)
            all_rows.extend(rows)
            city_runs.append(metadata)
            print(f"Fetched {len(rows)} forecast rows for {city['city']}")
        except Exception as exc:
            errors.append({"city": city["city"], "error": str(exc)})
            print(f"ERROR fetching {city['city']}: {exc}", file=sys.stderr)

    if not all_rows:
        raise RuntimeError(
            "No data was fetched. Check your internet connection and try again. "
            f"Errors: {errors}"
        )

    # Give every city in this run the same snapshot timestamp. This ensures
    # "latest snapshot" SQL queries include all cities even if API calls take
    # different amounts of time.
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for row in all_rows:
        row["fetched_at_utc"] = fetched_at

    df = transform_rows(all_rows)
    bad_rows = int(df["needs_review"].sum())
    quality = {
        "run_timestamp_utc": fetched_at,
        "rows_received": int(len(df)),
        "cities_configured": len(CITIES),
        "cities_succeeded": len(city_runs),
        "cities_failed": len(errors),
        "rows_needing_review": bad_rows,
        "duplicate_city_date_snapshot_rows": int(
            df.duplicated(["city", "forecast_date", "fetched_at_utc"]).sum()
        ),
        "passed_basic_quality_gate": bool(bad_rows == 0 and len(city_runs) == len(CITIES)),
        "errors": errors,
    }

    run_metadata = [{
        "run_timestamp_utc": fetched_at,
        "cities_configured": len(CITIES),
        "cities_succeeded": len(city_runs),
        "cities_failed": len(errors),
        "rows_loaded": len(df),
        "status": "SUCCESS" if not errors and bad_rows == 0 else "PARTIAL_OR_REVIEW",
    }]

    load_to_sqlite(df, run_metadata, quality)
    print("\nPipeline finished.")
    print(f"Rows loaded: {len(df)}")
    print(f"Rows needing review: {bad_rows}")
    print(f"Cities successful: {len(city_runs)}/{len(CITIES)}")
    print(f"SQLite database: {__import__('config').DB_PATH}")
    print(f"Reports folder: {REPORTS_DIR}")

if __name__ == "__main__":
    main()
