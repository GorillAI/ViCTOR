from victor.gpt_handler import analyze_user_request
from victor.itinerary import generate_itinerary
from victor.weather import get_weather
from victor.weather import generate_weather_intro  # Si tu as une fonction pour le résumé météo
from victor.database import get_pois
from config import GPT_VER, OPENAI_API_KEY
import openai, json


client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Main chatbot function
def chat_victor():
    """ Interactive chatbot function for Victor, the AI travel assistant. """
    print("\n🎒 Welcome to Victor, your AI travel assistant!")
    print("Type 'exit' to quit, 'restart' to start over.\n")

    while True:
        user_input = input("🗺️ Ask a travel question or request an itinerary: ").strip()

        if user_input.lower() == "exit":
            print("\n👋 Goodbye! Have a great trip!\n")
            break

        if user_input.lower() == "restart":
            print("\n🔄 Restarting... Describe your new request.\n")
            continue

        # Step 1: GPT analyzes the request
        print("\n🧠 Analyzing your request...\n")
        request_data = analyze_user_request(user_input)

        intent = request_data["intent"]
        language = request_data["language"]
        day_offset = 0

        if "tomorrow" in user_input.lower() or "demain" in user_input.lower():
            day_offset = 1
        elif "weekend" in user_input.lower() or "week-end" in user_input.lower():
            day_offset = 2

        # Handle general travel questions
        if intent == "general":
            print("\n💬 Answering your travel question...\n")
            response = generate_general_response(user_input, language)
            print(response)
            continue

        # Handle itinerary requests
        cities = request_data["cities"]
        print("\n✅ Detected itinerary:")
        for city in cities:
            print(f"- 📍 {city['name']} ({city['duration']}) - {', '.join(city['poi_types'])}")

        # Step 2: Retrieve real-time or forecast weather
        print("\n🌦️ Fetching weather information...\n")
        for city in cities:
            weather_info = get_weather(city["name"], language, day_offset)
            print(f"📍 Weather in {city['name']}: {weather_info if weather_info else 'Unavailable'}")

            # Step 3: Generate a weather-based introduction
            is_high_altitude = any("altitude" in poi_type.lower() for poi_type in city["poi_types"])
            weather_intro = generate_weather_intro(city["name"], weather_info, language, is_high_altitude)
            print(f"\n📢 {weather_intro}")

        # Step 4: Retrieve matching POIs
        pois = get_pois(cities)

        if not pois:
            print("⚠️ No results found. Try another city or attraction type.\n")
            continue

        # Step 5: Generate the itinerary
        print("\n✨ Generating your itinerary...\n")
        itinerary = generate_itinerary(cities, pois, user_input, language)
        print("\n📍 **Here is your optimized itinerary:**\n")
        print(itinerary)

        print("\n💡 You can refine your request or type 'restart' to ask another question.")

# Function to generate a general travel response
def generate_general_response(user_request, language):
    """ Generate a conversational response for general travel questions. """
    prompt = f"""
    You are a knowledgeable travel assistant. Answer the following user question in a helpful and structured way.
    Respond in the same language as the user request: {language}.

    User question: "{user_request}"
    """

    response = client.chat.completions.create(
        model=GPT_VER,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# Function to analyze user request and determine intent
def analyze_user_request(user_request):
    """ Extract structured data (cities, duration, POI types) and detect if the request is for an itinerary or general travel information. """
    prompt = f"""
    Analyze the following user request and determine if it is an itinerary request or a general travel question:
    "{user_request}"

    Return a JSON response with:
    - intent: "itinerary" if the user wants an itinerary, "general" if it's a travel-related question.
    - language: "fr", "en", etc.
    - cities (only if intent is "itinerary"): An array of cities with:
        - name: City name
        - duration: "morning", "afternoon", "full day"
        - poi_types: List of categories such as "culture", "nature", "gastronomy", etc.

    Example output for an itinerary request:
    {{
        "intent": "itinerary",
        "language": "fr",
        "cities": [
            {{ "name": "Vevey", "duration": "morning", "poi_types": ["culture", "gastronomy"] }},
            {{ "name": "Montreux", "duration": "afternoon", "poi_types": ["nature", "entertainment"] }}
        ]
    }}

    Example output for a general question:
    {{
        "intent": "general",
        "language": "en"
    }}
    """

    response = client.chat.completions.create(
        model=GPT_VER,
        messages=[{"role": "user", "content": prompt}]
    )

    structured_data = response.choices[0].message.content.strip()

    # Remove Markdown formatting if present
    if structured_data.startswith("```json"):
        structured_data = structured_data[7:-3].strip()

    return json.loads(structured_data)