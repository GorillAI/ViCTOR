# victor/intent_dispatcher.py

from victor.intent_map import get_modules_for_intent
from victor.weather import get_weather
from victor.database import get_pois
from victor.itinerary import generate_itinerary

# Placeholder imports for future modules
# from victor.events import get_events
# from victor.path_finder import get_paths
# from victor.transport import get_transport_info
# from victor.poi_info import explain_poi

def dispatch_intent(intent, parsed_data, user_input, language):
    """
    Executes the modules required for the detected intent.
    Returns a dictionary of results to feed into GPT.
    """
    modules = get_modules_for_intent(intent)
    results = {}

    for module in modules:
        if module == "weather":
            results["weather"] = []
            for city in parsed_data.get("cities", []):
                name = city.get("name")
                day_offset = parsed_data.get("day_offset", 0)
                forecast = get_weather(name, language, day_offset)
                results["weather"].append({"city": name, "forecast": forecast})

        elif module == "poi_selector":
            results["pois"] = get_pois(parsed_data.get("cities", []))

        elif module == "path_finder":
            results["paths"] = []  # get_paths(...) à implémenter

        elif module == "event_finder":
            results["events"] = []  # get_events(...) à implémenter

        elif module == "transport":
            results["transport_info"] = "Transport module placeholder"

        elif module == "poi_lookup":
            results["poi_info"] = "POI lookup module placeholder"

        elif module == "gpt_free":
            results["free_mode"] = True

    return results
