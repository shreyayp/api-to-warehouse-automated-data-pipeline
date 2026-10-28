# Data source and limitations

The dashboard uses the CSV bundled in `data/WeatherScope_PowerBI_Import.csv` for reproducible Power BI setup. The repository also contains a pipeline output at `data/processed/weather_forecast.csv`; compare the schemas before switching between the files.

The bundled import CSV contains 35 rows across five Indian cities and includes forecast dates, temperatures, precipitation, wind speed, and rain-risk/review flags. Verify the upstream source, retrieval timestamp, forecast horizon, units, and refresh process in the pipeline before describing the data as live or production-grade.

Do not commit API keys, credentials, or other secrets. If the dataset is replaced or refreshed, update this note and check the dashboard's measures and visual aggregations.
