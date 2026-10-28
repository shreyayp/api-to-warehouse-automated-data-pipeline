# API-to-Warehouse – Automated Data Pipeline

A Python-based ETL pipeline that retrieves weather forecasts from a public REST API, parses JSON responses, validates and transforms records, and loads structured data into a SQLite database. The project includes data quality checks, exception handling, automated tests, SQL analysis, and CSV/JSON reporting.

## Business question
How do forecast temperature, precipitation, and wind conditions differ across selected Indian cities over the next several days?

This is a learning project using public weather data, not an operational weather warning service.

## Tech stack
- Python 3.9+
- REST API / JSON
- Pandas
- SQLite and SQL
- Automated tests (`unittest`)
- CSV and JSON outputs
- Git-ready structure

## Data source and attribution
Open-Meteo Forecast API: https://open-meteo.com/en/docs  
API endpoint: `https://api.open-meteo.com/v1/forecast`  
Open-Meteo documents free access for non-commercial use without an API key, with attribution under CC BY 4.0. Review the current terms before public/commercial reuse: https://open-meteo.com/en/features#terms

Forecasts update over time. Results are snapshots taken when the pipeline runs; this project does not claim guaranteed real-time uptime or forecast accuracy.

## Run on macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.pipeline
python -m unittest discover -s tests -v
```

## Run on Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.pipeline
python -m unittest discover -s tests -v
```

Internet access is required to call the API. If the API is temporarily unavailable, the script reports the failure instead of silently fabricating data.

## Outputs
- `data/processed/weather_forecast.csv`: normalized forecast rows
- `data/processed/weather_pipeline.db`: SQLite database
- `reports/city_forecast_summary.csv`: city-level summary
- `reports/rain_risk_days.csv`: days with precipitation probability at or above configured threshold
- `reports/data_quality_report.json`: validation outcomes
- `reports/latest_run.json`: run metadata

## What to learn
1. REST API and HTTP status codes
2. JSON response structure
3. Data normalization and type conversion
4. Data quality rules and failure handling
5. SQLite tables and append-only forecast snapshots
6. SQL aggregations
7. Unit testing
8. Documentation and reproducibility

## Limitations
- Forecasts are model outputs and can change between runs.
- The selected cities are a small sample, not all of India.
- Precipitation probability is not the same as expected rainfall amount.
- The project stores forecast snapshots, not verified observed weather.
- Do not claim this is production monitoring until scheduling, alerting, and deployment are actually configured.
