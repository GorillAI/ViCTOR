from victor.gpt_handler import analyze_user_request
from victor.itinerary import generate_itinerary

def chat_victor():
    """ Interactive chatbot function for Victor, the AI travel assistant. """
    print("\n🎒 Welcome to Victor, your AI travel assistant!")
    print("Type 'exit' to quit, 'restart' to start over.\n")

    while True:
        user_input = input("🗺️ Ask a travel question or request an itinerary: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("\n👋 Goodbye! Have a great trip!\n")
            break

        if user_input.lower() == "restart":
            print("\n🔄 Restarting...\n")
            continue

        print("\n🧠 Analyzing your request...\n")
        request_data = analyze_user_request(user_input)
        intent = request_data.get("intent", "general")
        language = request_data.get("language", "en")

        if intent == "general":
            print("\n💬 Answering your general travel question...\n")
        else:
            city = input("📍 Enter city: ").strip()
            categories = input("🎭 Enter POI categories (comma-separated): ").strip().split(",")
            day_offset = int(input("📅 Enter day offset (0=today, 1=tomorrow): ").strip())
            
            itinerary = generate_itinerary(city, categories, day_offset, language)
            print("\n📍 **Your itinerary:**\n")
            print(itinerary)
