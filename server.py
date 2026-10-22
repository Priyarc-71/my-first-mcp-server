
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

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            geo_response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
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
                    "error": f"City '{city}' was not found."
                }

            place = geo_data["results"][0]

            weather_response = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
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
            return {"error": "Weather data is unavailable."}

        conditions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            80: "Rain showers",
            81: "Moderate rain showers",
            82: "Heavy rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with hail"
        }

        return {
            "city": place["name"],
            "country": place.get("country", "Unknown"),
            "temperature_c": weather["temperature_2m"],
            "feels_like_c": weather["apparent_temperature"],
            "humidity_percent": weather["relative_humidity_2m"],
            "condition": conditions.get(
                weather["weather_code"], "Other conditions"
            ),
            "wind_speed_kmh": weather["wind_speed_10m"],
            "updated_at": weather["time"],
            "timezone": data.get("timezone")
        }

    except Exception as error:
        return {
            "error": f"{type(error).__name__}: {error}"
        }


async def main():
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
