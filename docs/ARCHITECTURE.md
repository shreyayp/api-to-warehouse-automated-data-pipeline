# Architecture

1. `src/extract.py` calls Open-Meteo's forecast endpoint for each configured city and parses daily JSON arrays into row records.
2. `src/transform.py` converts dates and numbers, derives temperature range and a configurable precipitation-risk flag, and records quality issues.
3. `src/load.py` appends forecast snapshots and run/quality metadata to SQLite and exports summary CSV/JSON reports.
4. `src/pipeline.py` orchestrates the steps, reports per-city failures, and avoids pretending a partial API failure was a complete success.

## Tables
- `weather_forecast`: one city × forecast date × fetched timestamp row.
- `pipeline_runs`: one record per pipeline run.
- `quality_checks`: one record per quality report.

Repeated runs preserve historical forecast snapshots; forecasts may change because models are updated. `fetched_at_utc` allows users to compare what the API predicted at different times.
