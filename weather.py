import requests
from datetime import datetime

API_KEY = "a142f5b410c4de1723204d01be94a523"

CITY = input("Enter city name: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

if data.get("cod") != 200:
    print("Error:", data.get("message"))
else:
    print("City:", data["name"])
    print("Temperature:", data["main"]["temp"], "°C")
    print("Humidity:", data["main"]["humidity"], "%")
    print("Weather:", data["weather"][0]["main"])
    print("Description:", data["weather"][0]["description"])
    print("Wind Speed:", data["wind"]["speed"], "m/s")

    dt = datetime.fromtimestamp(data["dt"])
    print("Date & Time:", dt)








