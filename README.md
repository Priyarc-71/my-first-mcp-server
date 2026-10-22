MCP Intern Project — Day 1
Objective
Connect existing MCP servers and inspect their tools using MCP Inspector.

Concepts

Host
The AI application the user interacts with. It runs the model.

Client
The component inside the host that communicates with an MCP server.

Server
The program that exposes tools, resources, and prompts to an AI application.

Day 1 Tasks
-  Check the development environment.
-  Connect the Filesystem MCP server.
-  Connect the GitHub MCP server.
-  Capture one `tools/list` exchange.
-  Capture one `tools/call` exchange.
-  Test the servers and record the results.


My First MCP Server

Overview
A Python MCP server that provides mathematical tools.

Features
- Add two numbers
- Multiply two numbers
- Project information resource
- Math helper prompt
- Basic input validation

Requirements
- Python 3.13
- MCP Python SDK 2.x

Run
Activate the virtual environment and run:

powershell
python server.py

For testing, connect the server to MCP Inspector using STDIO.

Tools
- add_numbers(a, b)
- multiply_numbers(a, b)

Resource
- info://project

Prompt
- math_helper(operation)


Weather Checker MCP Server

Project Overview
This project is a Model Context Protocol (MCP) server that provides current weather information for cities worldwide. It connects to Ollama using the Qwen3 4B model, allowing users to ask weather questions in natural language.

 Features
- Search for cities worldwide.
- Get current temperature in Celsius.
- Get feels-like temperature.
- Get humidity percentage.
- Get weather conditions.
- Get wind speed.
- Display local update time and timezone.
- Handle empty and unknown city names.
- Use Ollama to ask weather questions in natural language.

 Technologies Used
- Python
- MCP SDK 2.x
- HTTPX
- Ollama
- Qwen3 4B
- Open-Meteo Geocoding API
- Open-Meteo Weather API
- Python unittest

 Project Files
- `server.py` — MCP server and weather tool.
- `weather_client.py` — Connects Ollama to the MCP server.
- `test_weather.py` — Automated tests for weather functionality.
- `README.md` — Project documentation.

 Requirements
- Python 3.13
- Ollama
- Qwen3 4B model
- Internet connection

Setup

1. Install dependencies

```bash
python -m pip install "mcp[cli]" httpx ollama
```

2. Download the Ollama model

```bash
ollama pull qwen3:4b
```

3. Run the Weather MCP client

Make sure Ollama is running, then execute:

```bash
python weather_client.py
```

Enter a question, for example:

`What is the current weather in Hyderabad?`

The client connects to the MCP server, calls the weather tool, and displays the result with Ollama's response.

Available MCP Tool

`check_weather(city)`

Accepts a city name and returns its current weather information, including temperature, feels-like temperature, humidity, conditions, wind speed, update time, and timezone.

Automated Testing

Run the tests using:

bash
python -m unittest test_weather -v


Three automated tests are included:

1. `test_valid_city` — checks a valid city response.
2. `test_empty_city` — checks empty input handling.
3. `test_unknown_city` — checks handling of an unknown city.

All three tests passed during project testing. The tests use simulated API responses and do not replace live API testing.

APIs Used
- Geocoding API: https://geocoding-api.open-meteo.com/
- Weather API: https://open-meteo.com/

Author
Priya R C


