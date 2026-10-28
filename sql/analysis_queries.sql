-- 1. Latest forecast snapshot by city: compare temperature and precipitation.
SELECT city,
       ROUND(AVG(temperature_2m_max), 1) AS avg_max_temp_c,
       ROUND(MAX(temperature_2m_max), 1) AS highest_max_temp_c,
       ROUND(SUM(precipitation_sum), 1) AS forecast_precipitation_mm
FROM weather_forecast
WHERE fetched_at_utc = (SELECT MAX(fetched_at_utc) FROM weather_forecast)
GROUP BY city
ORDER BY avg_max_temp_c DESC;

-- 2. Days with at least 50% precipitation probability.
SELECT city, forecast_date, precipitation_probability_max, precipitation_sum
FROM weather_forecast
WHERE fetched_at_utc = (SELECT MAX(fetched_at_utc) FROM weather_forecast)
  AND precipitation_probability_max >= 50
ORDER BY precipitation_probability_max DESC, city, forecast_date;

-- 3. Check data quality flags.
SELECT city, forecast_date, quality_flags
FROM weather_forecast
WHERE needs_review = 1;

-- 4. Compare the same city's forecast snapshots across pipeline runs.
SELECT city, forecast_date, fetched_at_utc, temperature_2m_max,
       precipitation_probability_max
FROM weather_forecast
WHERE city = 'Bengaluru'
ORDER BY forecast_date, fetched_at_utc DESC;
