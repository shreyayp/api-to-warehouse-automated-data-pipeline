# Portfolio and interview guide

## Suggested resume bullets — use only after successfully running and reviewing the project
- Built a Python REST API ingestion pipeline to collect daily weather forecasts for five Indian cities, normalize JSON responses with Pandas, and load validated records into SQLite.
- Implemented data quality checks for required fields, date validity, temperature consistency, precipitation probability bounds, and negative wind speeds.
- Developed SQL summaries and CSV reports to compare city-level temperature, precipitation, and wind forecasts; retained timestamped snapshots for forecast-change analysis.
- Added unit tests and documented setup steps for macOS and Windows.

## Explain the pipeline
1. Extract: call a documented public REST endpoint.
2. Transform: parse types, derive temperature range, flag suspicious records.
3. Load: append rows to SQLite and export reports.
4. Validate: test transformation rules and record pipeline status.
5. Analyse: use SQL to compare forecast values by city/date.

## Limitations to explain honestly
- This is forecast data, not verified observed weather.
- Forecasts may change between runs.
- It is a five-city sample.
- A 50% precipitation-probability threshold is a project rule, not an official severe-weather warning.
- No automatic scheduler or production alerting is configured in the starter version.
