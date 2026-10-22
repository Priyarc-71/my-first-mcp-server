
import unittest
from unittest.mock import patch, AsyncMock, Mock

from server import check_weather


class TestWeather(unittest.IsolatedAsyncioTestCase):

    @patch("server.httpx.AsyncClient")
    async def test_valid_city(self, mock_client):
        client = AsyncMock()
        mock_client.return_value.__aenter__.return_value = client

        geo_response = Mock()
        geo_response.json.return_value = {
            "results": [{
                "name": "Mumbai",
                "country": "India",
                "latitude": 19.07,
                "longitude": 72.87
            }]
        }
        geo_response.raise_for_status.return_value = None

        weather_response = Mock()
        weather_response.json.return_value = {
            "current": {
                "temperature_2m": 29.6,
                "apparent_temperature": 32.3,
                "relative_humidity_2m": 55,
                "weather_code": 1,
                "wind_speed_10m": 6,
                "time": "2026-10-23T02:00"
            },
            "timezone": "Asia/Kolkata"
        }
        weather_response.raise_for_status.return_value = None

        client.get.side_effect = [geo_response, weather_response]

        result = await check_weather("Mumbai")

        self.assertEqual(result["city"], "Mumbai")
        self.assertEqual(result["temperature_c"], 29.6)
        self.assertEqual(result["condition"], "Mainly clear")

    async def test_empty_city(self):
        result = await check_weather(" ")
        self.assertIn("error", result)

    @patch("server.httpx.AsyncClient")
    async def test_unknown_city(self, mock_client):
        client = AsyncMock()
        mock_client.return_value.__aenter__.return_value = client

        response = Mock()
        response.json.return_value = {}
        response.raise_for_status.return_value = None
        client.get.return_value = response

        result = await check_weather("xyzabc123")

        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
