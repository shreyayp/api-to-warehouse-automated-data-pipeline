import unittest
from src.transform import transform_rows

def sample_row(**overrides):
    row = {
        "city": "Bengaluru",
        "country": "India",
        "latitude": 12.97,
        "longitude": 77.59,
        "forecast_date": "2026-10-22",
        "fetched_at_utc": "2026-10-22T10:00:00+00:00",
        "weather_code": 3,
        "temperature_2m_max": 30.0,
        "temperature_2m_min": 20.0,
        "precipitation_sum": 2.5,
        "precipitation_probability_max": 60,
        "wind_speed_10m_max": 15.0,
    }
    row.update(overrides)
    return row

class TransformTests(unittest.TestCase):
    def test_temperature_range(self):
        df = transform_rows([sample_row()])
        self.assertEqual(df.loc[0, "temperature_range_c"], 10.0)

    def test_rain_risk_flag(self):
        df = transform_rows([sample_row(precipitation_probability_max=60)])
        self.assertTrue(bool(df.loc[0, "is_rain_risk"]))

    def test_invalid_probability_flagged(self):
        df = transform_rows([sample_row(precipitation_probability_max=140)])
        self.assertTrue(bool(df.loc[0, "needs_review"]))
        self.assertIn("invalid_precipitation_probability", df.loc[0, "quality_flags"])

    def test_min_greater_than_max_flagged(self):
        df = transform_rows([sample_row(temperature_2m_min=35, temperature_2m_max=25)])
        self.assertIn("min_temperature_above_max", df.loc[0, "quality_flags"])

if __name__ == "__main__":
    unittest.main()
