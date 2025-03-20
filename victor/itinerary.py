from victor.database import get_pois
from victor.weather import get_weather

def generate_itinerary(city, categories, day_offset, language):
    """ Generate an itinerary based on POIs and weather conditions. """
    pois = get_pois(city, categories)
    weather_info = get_weather(city, language, day_offset)

    itinerary = f"🌦️ Weather in {city}: {weather_info}\n\nSuggested itinerary:\n"

    for poi in pois:
        itinerary += f"- {poi[0]} ({poi[2]}) - {poi[3]} CHF - {poi[4]} min\n"

    return itinerary
