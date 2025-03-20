from victor.database import get_pois
from victor.weather import get_weather
from config import GPT_VER, OPENAI_API_KEY
import openai


client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Function to generate an itinerary using GPT
def generate_itinerary(cities, pois, user_request, language):
    """ Generate an optimized itinerary using GPT-4 Turbo in the user's language. """

    pois_str = "\n".join([
        f"- {name} ({city} - {poi_type}) - {price} CHF - {time} min"
        for name, city, poi_type, price, time, _, _ in pois
    ])

    prompt = f"""
    You are an AI travel assistant. Here is a list of available attractions for the user's multi-city request:

    {pois_str}

    Create an optimized itinerary based on the following user request:
    "{user_request}"

    Make sure to organize the itinerary by city, keeping the requested duration for each location.
    The response should be structured and easy to read.

    Respond in the same language as the user's request: {language}.
    """

    response = client.chat.completions.create(
        model=GPT_VER,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

