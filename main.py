from victor.weather import get_weather
from victor.database import get_pois

def main():
    city = input("Enter a city: ").strip()
    day_offset = int(input("Enter day offset (0=today, 1=tomorrow): ").strip())

    # Fetch weather
    weather = get_weather(city, "fr", day_offset)
    print(f"🌦️ Weather for {city}: {weather}")

    # Fetch POIs
    pois = get_pois(city, ["culture", "nature"])
    print("🔎 Recommended places:")
    for poi in pois:
        print(f"- {poi[0]} ({poi[2]}) - {poi[3]} CHF - {poi[4]} min")

if __name__ == "__main__":
    main()
