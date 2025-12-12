from waether_api import get_weather
from utils import display_weather

API_KEY = "f77b1848275b9a4988d1fc46b7da2eb6"  # Replace with your OpenWeatherMap API key

def main():
    city = input("Enter city name: ")
    data = get_weather(city, API_KEY)

    if data:
        display_weather(data)
    else:
        print("\n❌ City not found or invalid API key!")

if __name__ == "__main__":
    main()
