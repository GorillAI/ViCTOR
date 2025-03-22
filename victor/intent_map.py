# victor/intent_map.py

INTENT_MAP = {
    "itinerary_generation": {
        "description": "Create a structured itinerary with POIs, weather, and path suggestions.",
        "modules": ["weather", "poi_selector", "path_finder", "itinerary"]
    },

    "ask_recommendation": {
        "description": "Suggest activities, walks, restaurants, or experiences.",
        "modules": ["weather", "poi_selector", "path_finder", "event_finder"]
    },

    "weather_info": {
        "description": "Provide weather forecast for a city and date.",
        "modules": ["weather"]
    },

    "event_check": {
        "description": "List events happening in a city or region.",
        "modules": ["event_finder"]
    },

    "poi_explanation": {
        "description": "Explain what a specific location or POI is.",
        "modules": ["poi_lookup"]
    },

    "transport_info": {
        "description": "Provide directions or transport options between places.",
        "modules": ["transport"]
    },

    "general_query": {
        "description": "Handle general or vague questions using GPT freely.",
        "modules": ["gpt_free"]
    }
}

def get_modules_for_intent(intent):
    return INTENT_MAP.get(intent, {}).get("modules", [])

def get_description_for_intent(intent):
    return INTENT_MAP.get(intent, {}).get("description", "No description available.")
