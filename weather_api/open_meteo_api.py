import requests

def get_weather_data(url: str = "https://api.open-meteo.com/v1/forecast?", latitude: float = 23.7591286, longitude: float = 90.4277264) -> dict:
    params={
        "latitude": latitude,
        "longitude": longitude,
        # "hourly": "temperature_2m", # Uncomment if you want hourly data
        "current": "temperature_2m", # Use "current" for current weather data
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch weather data"}

if __name__ == "__main__":
    weather_data = get_weather_data()
    print(weather_data)