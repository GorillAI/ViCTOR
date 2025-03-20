import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key. Set the environment variable OPENAI_API_KEY.")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def analyze_user_request(user_request):
    """ Analyze user request and determine whether it's for an itinerary or general travel info. """
    prompt = f"""
    Analyze the following user request and determine if it is an itinerary request or a general travel question:
    "{user_request}"

    Return a JSON response with:
    - intent: "itinerary" if the user wants an itinerary, "general" if it's a travel-related question.
    - language: "fr", "en", etc.
    """

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
