
import asyncio
import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Weather Checker")


@mcp.tool()
async def check_weather(city: str) -> dict:
    """Get current weather for any city worldwide."""

    city = city.strip()

    if not city:
        return {"error": "Please enter a city name."}

    async with httpx.AsyncClient(timeout=20) as client:
        # Find the city
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = await client.get(
            geo_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {
                "error": f"Could not find the city '{city}'. "
                         "Check the spelling or try a nearby city."
            }

        place = geo_data["results"][0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        # Get current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"

        weather_response = await client.get(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            }
        )
        weather_response.raise_for_status()
        data = weather_response.json()

    weather = data.get("current")

    if not weather:
        return {"error": "Weather data is currently unavailable."}

    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }

    return {
        "city": place["name"],
        "country": place.get("country", "Unknown"),
        "temperature_c": weather["temperature_2m"],
        "feels_like_c": weather["apparent_temperature"],
        "humidity_percent": weather["relative_humidity_2m"],
        "condition": weather_codes.get(
            weather["weather_code"], "Unknown conditions"
        ),
        "wind_speed_kmh": weather["wind_speed_10m"],
        "updated_at": weather["time"],
        "timezone": data.get("timezone")
    }


async def main():
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
