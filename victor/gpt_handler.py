import openai
import os
import json
from config import OPENAI_API_KEY, GPT_VER

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def analyze_user_request(user_request):
    """
    Use GPT to extract structured data from a free-text travel request.
    Returns a dict with:
    - intent: "itinerary_generation" or "general"
    - language: "fr", "en", etc.
    - day_offset: 0 = today, 1 = tomorrow, etc.
    - cities: [
        { "name": "Vevey", "duration": "morning", "poi_types": ["nature", "gastronomy"] },
        ...
      ]
    """
    prompt = f"""
You are an assistant that extracts structured data from a user's travel request.

Request:
\"{user_request}\"

Return a JSON object with:
- intent: "itinerary_generation" or "general"
- language: detected language code (e.g., "fr", "en")
- day_offset: 0 if the user means today, 1 for tomorrow, etc.
- cities: a list of cities involved in the trip. For each:
    - name: the name of the city
    - duration: "morning", "afternoon", "full day"
    - poi_types: list of categories like "culture", "nature", "gastronomy", "romantic", etc.

Example output:
{{
  "intent": "itinerary_generation",
  "language": "fr",
  "day_offset": 1,
  "cities": [
    {{
      "name": "Vevey",
      "duration": "morning",
      "poi_types": ["romantic", "nature"]
    }},
    {{
      "name": "Montreux",
      "duration": "afternoon",
      "poi_types": ["culture"]
    }}
  ]
}}
Only return valid JSON.
    """

    response = client.chat.completions.create(
        model=GPT_VER,
        messages=[{"role": "user", "content": prompt}]
    )

    structured = response.choices[0].message.content.strip()

    # Remove markdown formatting if GPT added ```json
    if structured.startswith("```json"):
        structured = structured[7:-3].strip()

    return json.loads(structured)

