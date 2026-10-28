# Data dictionary

| Field | Meaning | Unit/type |
|---|---|---|
| city | Configured city | Text |
| country | Country | Text |
| latitude / longitude | Requested coordinates | Decimal degrees |
| forecast_date | Forecast day | ISO date |
| fetched_at_utc | When this snapshot was fetched | UTC timestamp |
| weather_code | WMO-style weather code from provider | Integer |
| temperature_2m_max | Daily maximum temperature at 2m | °C |
| temperature_2m_min | Daily minimum temperature at 2m | °C |
| temperature_range_c | Maximum minus minimum temperature | °C |
| precipitation_sum | Forecast daily precipitation total | mm |
| precipitation_probability_max | Maximum precipitation probability | % |
| wind_speed_10m_max | Maximum wind speed at 10m | km/h |
| is_rain_risk | True when probability is >= 50% | Boolean |
| quality_flags | Semicolon-separated review flags | Text |
| needs_review | One or more quality flags exist | Boolean |
