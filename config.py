"""Project configuration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = ROOT / "reports"
DB_PATH = PROCESSED_DIR / "weather_pipeline.db"
CSV_PATH = PROCESSED_DIR / "weather_forecast.csv"

API_URL = "https://api.open-meteo.com/v1/forecast"
FORECAST_DAYS = 7
RAIN_PROBABILITY_THRESHOLD = 50

CITIES = [
    {"city": "Bengaluru", "country": "India", "latitude": 12.9716, "longitude": 77.5946},
    {"city": "Mysuru", "country": "India", "latitude": 12.2958, "longitude": 76.6394},
    {"city": "Chennai", "country": "India", "latitude": 13.0827, "longitude": 80.2707},
    {"city": "Hyderabad", "country": "India", "latitude": 17.3850, "longitude": 78.4867},
    {"city": "Mumbai", "country": "India", "latitude": 19.0760, "longitude": 72.8777},
]
