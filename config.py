import os

# Clés API (doivent être définies dans .env ou en variable d'environnement)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ Missing OpenAI API key. Define it in a .env file or as an environment variable.")

if not WEATHER_API_KEY:
    raise ValueError("⚠️ Missing OpenWeatherMap API key. Define it in a .env file or as an environment variable.")

# Chemin de la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "Victor_locations.db")
