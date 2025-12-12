import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city, api_key):
    url = f"{BASE_URL}?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data.get("cod") == 200:
        return data
    else:
        return None
