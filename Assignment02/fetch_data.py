import requests
import json

url = "https://jsonplaceholder.typicode.com/posts"

# Fetch API data
response = requests.get(url)

# Convert JSON to Python list/dict
data = response.json()

# Save to a file
with open("posts.json", "w") as file:
    json.dump(data, file, indent=4)

print("Data fetched and saved to posts.json")
