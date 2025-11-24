from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import httpx
import re
from datetime import datetime

router = APIRouter()

class WeatherRequest(BaseModel):
    user_input: str

# Mock data as fallback
MOCK_WEATHER_DATA = {
    "Beijing": {
        "temperature": 28, "condition": "Sunny", "humidity": 45, "wind": "Southeast Wind Level 3",
        "air_quality": "Good", "aqi": 78, "feels_like": 30, "uv_index": 6,
        "visibility": 10, "pressure": 1013, "dew_point": 18,
        "forecast": [
            {"date": "Tomorrow", "max": 30, "min": 20, "condition": "Sunny", "emoji": "☀️"},
            {"date": "Day after", "max": 32, "min": 22, "condition": "Cloudy", "emoji": "☁️"},
            {"date": "3 Days", "max": 29, "min": 19, "condition": "Rain", "emoji": "🌧️"}
        ]
    }
}

async def get_coordinates(city: str) -> Optional[Dict[str, float]]:
    """
    Get coordinates for a city using Open-Meteo Geocoding API
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("results"):
                return None
                
            result = data["results"][0]
            return {
                "lat": result["latitude"],
                "lon": result["longitude"],
                "name": result["name"],
                "country": result.get("country", "")
            }
    except Exception as e:
        print(f"Error fetching coordinates for {city}: {e}")
        return None

def get_wmo_description(code: int) -> tuple[str, str]:
    """
    Map WMO weather code to description and emoji
    """
    codes = {
        0: ("Clear sky", "☀️"), 1: ("Mainly clear", "☀️"), 2: ("Partly cloudy", "⛅"), 3: ("Overcast", "☁️"),
        45: ("Fog", "🌫️"), 48: ("Depositing rime fog", "🌫️"),
        51: ("Light drizzle", "🌦️"), 53: ("Moderate drizzle", "🌦️"), 55: ("Dense drizzle", "🌧️"),
        56: ("Light freezing drizzle", "🌧️"), 57: ("Dense freezing drizzle", "🌧️"),
        61: ("Slight rain", "🌦️"), 63: ("Moderate rain", "🌧️"), 65: ("Heavy rain", "⛈️"),
        66: ("Light freezing rain", "🌧️"), 67: ("Heavy freezing rain", "⛈️"),
        71: ("Slight snow fall", "❄️"), 73: ("Moderate snow fall", "❄️"), 75: ("Heavy snow fall", "❄️"),
        77: ("Snow grains", "❄️"),
        80: ("Slight rain showers", "🌦️"), 81: ("Moderate rain showers", "🌧️"), 82: ("Violent rain showers", "⛈️"),
        85: ("Slight snow showers", "❄️"), 86: ("Heavy snow showers", "❄️"),
        95: ("Thunderstorm", "⚡"), 96: ("Thunderstorm with slight hail", "⚡❄️"), 99: ("Thunderstorm with heavy hail", "⚡❄️")
    }
    return codes.get(code, ("Unknown", "🌡️"))

async def get_weather_from_open_meteo(lat: float, lon: float) -> Optional[Dict[str, Any]]:
    """
    Fetch weather data from Open-Meteo (Current + Daily Forecast)
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Fetch current weather and daily forecast (max/min temp, weather code)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,visibility&daily=weather_code,temperature_2m_max,temperature_2m_min,uv_index_max&timezone=auto&forecast_days=4"
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            current = data["current"]
            daily = data.get("daily", {})
            
            condition, emoji = get_wmo_description(current["weather_code"])
            
            # Process Forecast (Next 3 days, skipping today index 0 usually, or showing today + next 2)
            # Let's show Today + Next 2 days
            forecast = []
            if daily:
                for i in range(1, 4): # Get next 3 days (indices 1, 2, 3)
                    if i < len(daily["time"]):
                        code = daily["weather_code"][i]
                        desc, icon = get_wmo_description(code)
                        date_str = daily["time"][i] # YYYY-MM-DD
                        
                        # Simple date formatting
                        try:
                            dt = datetime.strptime(date_str, "%Y-%m-%d")
                            formatted_date = dt.strftime("%a, %b %d") # Mon, Jan 01
                        except:
                            formatted_date = date_str

                        forecast.append({
                            "date": formatted_date,
                            "max": int(daily["temperature_2m_max"][i]),
                            "min": int(daily["temperature_2m_min"][i]),
                            "condition": desc,
                            "emoji": icon
                        })

            # Get UV index (max for today)
            uv_index = 0
            if daily.get("uv_index_max") and len(daily["uv_index_max"]) > 0:
                uv_index = daily["uv_index_max"][0]

            return {
                "temperature": int(current["temperature_2m"]),
                "condition": condition,
                "emoji": emoji,
                "humidity": int(current["relative_humidity_2m"]),
                "wind": f"{current['wind_speed_10m']} km/h",
                "air_quality": "N/A",
                "aqi": 0,
                "feels_like": int(current["apparent_temperature"]),
                "uv_index": int(uv_index) if uv_index is not None else 0,
                "visibility": int(current.get("visibility", 10000) / 1000),
                "pressure": int(current["surface_pressure"]),
                "dew_point": 0,
                "forecast": forecast
            }
    except Exception as e:
        print(f"Error fetching weather from Open-Meteo: {e}")
        return {"error": str(e)}

def extract_city_from_text(text: str) -> Optional[str]:
    text = text.strip()
    match = re.search(r"weather\s+(?:in|of|at|like\s+in)\s+([a-zA-Z\s\u4e00-\u9fa5]+)", text, re.IGNORECASE)
    if match:
        candidate = match.group(1).strip()
        if candidate.lower().startswith("weather in"):
            candidate = candidate[10:].strip()
        return candidate.title()
    
    common_cities = [
        "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu", "Hangzhou", "Xi'an", "Chongqing",
        "London", "New York", "Tokyo", "Paris", "Sydney", "Hong Kong", "Singapore", "Berlin",
        "Los Angeles", "Chicago", "Toronto", "Vancouver", "Dubai", "Mumbai", "Bangkok", "Seoul"
    ]
    for city in common_cities:
        if city.lower() in text.lower():
            return city
            
    if len(text) < 20 and "weather" not in text.lower() and re.match(r"^[a-zA-Z\s\u4e00-\u9fa5]+$", text):
        return text.title()
    return None

def get_uv_advice(uv_index: int) -> str:
    if uv_index <= 2: return "Low"
    elif uv_index <= 5: return "Moderate"
    elif uv_index <= 7: return "High"
    elif uv_index <= 10: return "Very High"
    else: return "Extreme"

@router.post("/query")
async def query_weather(request: WeatherRequest):
    text = request.user_input
    city = extract_city_from_text(text)

    if not city:
        return {
            "bot_response": """🌤️ Weather Assistant

I couldn't identify the city. Please try:
• "Beijing"
• "Weather in Shanghai"
• "London weather"
""",
            "suggestions": ["Beijing", "Shanghai", "London"]
        }

    # 1. Get Coordinates
    coords = await get_coordinates(city)
    if not coords:
        return {
            "bot_response": f"Sorry, I couldn't find the location **{city}**. Please check the spelling.",
            "suggestions": ["Beijing", "Shanghai"]
        }
    
    real_city_name = coords["name"]
    country = coords["country"]

    # 2. Get Weather
    weather = await get_weather_from_open_meteo(coords["lat"], coords["lon"])
    source = "Open-Meteo"
    
    if not weather or weather.get("error"):
        error_msg = weather.get("error") if weather else "Unknown error"
        print(f"API failed for {city}: {error_msg}. Falling back to mock data.")
        weather = MOCK_WEATHER_DATA.get(city)
        source = "mock data (API failed)"
        
        if not weather:
            return {
                "bot_response": f"Sorry, I couldn't fetch weather data for **{real_city_name}** ({error_msg}).",
                "suggestions": ["Beijing", "Shanghai"]
            }
        else:
            weather["emoji"] = "🌡️"

    emoji = weather.get("emoji", "🌡️")
    
    # Format Forecast
    forecast_text = ""
    if weather.get("forecast"):
        forecast_text = "\n\n📅 **Forecast**:\n"
        for day in weather["forecast"]:
            forecast_text += f"• **{day['date']}**: {day['emoji']} {day['max']}°C / {day['min']}°C ({day['condition']})\n"

    response_text = f"""{emoji} **Weather in {real_city_name}, {country}**

🌡️ **Temperature**: {weather["temperature"]}°C (Feels like {weather["feels_like"]}°C)
☁️ **Condition**: {weather["condition"]}
💧 **Humidity**: {weather["humidity"]}%
💨 **Wind**: {weather["wind"]}
☀️ **UV Index**: {weather["uv_index"]} ({get_uv_advice(weather["uv_index"])})
👁️ **Visibility**: {weather["visibility"]} km
🔵 **Pressure**: {weather["pressure"]} hPa{forecast_text}

🔄 Source: {source}"""

    return {
        "bot_response": response_text,
        "data": {
            "city": real_city_name,
            **weather
        }
    }