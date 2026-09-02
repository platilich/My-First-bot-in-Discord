import requests

def get_weather(city: str):
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1, "language": "en"}
    ).json()

    if not geo.get("results"):
        return f"City '{city}' not found"

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    city_name = geo["results"][0]["name"]

    data = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code",
            "timezone": "auto"
        }
    ).json()

    cur = data["current"]

    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy",
        3: "Overcast", 45: "Fog", 48: "Rime fog",
        51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
        61: "Light rain", 63: "Rain", 65: "Heavy rain",
        71: "Light snow", 73: "Snow", 75: "Heavy snow",
        80: "Rain showers", 95: "Thunderstorm"
    }

    result = f"{city_name}\n\n"
    result += f"{cur['temperature_2m']}°C (feels like {cur['apparent_temperature']}°C)\n"
    result += f"Humidity: {cur['relative_humidity_2m']}%\n"
    result += f"Wind: {cur['wind_speed_10m']} km/h\n"
    result += f"{codes.get(cur['weather_code'], 'Unknown')}"

    return result