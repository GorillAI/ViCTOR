# victor/chatbot.py

from victor.gpt_handler import analyze_user_request
from victor.intent_dispatcher import dispatch_intent
from victor.itinerary import generate_itinerary
# from victor.response_generator import gpt_generate_response  # si tu veux gérer les autres réponses

def chat_victor():
    print("\n🎒 Welcome to ViCTOR — your personal travel assistant")
    print("Type 'exit' to quit or 'restart' to start over.\n")

    while True:
        user_input = input("💬 You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("\n👋 Goodbye! Safe travels!\n")
            break

        if user_input.lower() == "restart":
            print("\n🔄 Let's start again.\n")
            continue

        print("\n🧠 Analyzing your request...\n")
        parsed = analyze_user_request(user_input)
        intent = parsed.get("intent", "general_query")
        language = parsed.get("language", "en")
        cities = parsed.get("cities", [])

        print(f"🧭 Intent detected: {intent}")
        print("📍 Locations:")
        for city in cities:
            print(f" - {city['name']} ({city['duration']}) – {', '.join(city['poi_types'])}")

        print("\n⚙️ Gathering contextual data...\n")
        context = dispatch_intent(intent, parsed, user_input, language)

        if intent == "itinerary_generation":
            pois = context.get("pois", [])
            response = generate_itinerary(cities, pois, user_input, language)
        else:
            # Placeholder: return raw context (until a proper GPT response generator is made)
            response = f"\n[Contextual Data Collected for GPT]\n{context}"

        print("\n🧾 ViCTOR says:\n")
        print(response)
