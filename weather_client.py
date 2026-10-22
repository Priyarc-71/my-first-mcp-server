
import asyncio
import json
import ollama

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command=r"C:\Users\priya\OneDrive\Desktop\mcp-intern-priya\.venv\Scripts\python.exe",
    args=[
        r"C:\Users\priya\OneDrive\Desktop\mcp-intern-priya\server.py"
    ]
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()

            tools = []

            for tool in tools_result.tools:
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.input_schema
                    }
                })

            question = input("Ask about the weather: ")

            response = ollama.chat(
                model="qwen3:4b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a weather assistant. "
                            "Use check_weather for weather questions. "
                            "Never invent weather data."
                        )
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                tools=tools
            )

            message = response["message"]
            tool_calls = message.get("tool_calls", [])

            if not tool_calls:
                print("\nOllama's answer:")
                print(message["content"])
                return

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Answer weather questions using the actual "
                        "results returned by the weather tool."
                    )
                },
                {
                    "role": "user",
                    "content": question
                },
                message
            ]

            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]

                print(f"\nCalling MCP tool: {tool_name}")

                result = await session.call_tool(
                    tool_name,
                    arguments
                )

                tool_output = []

                for item in result.content:
                    if hasattr(item, "text"):
                        tool_output.append(item.text)

                result_text = "\n".join(tool_output)

                print("Weather tool result:")
                print(result_text)

                messages.append({
                    "role": "tool",
                    "content": result_text
                })

            final_response = ollama.chat(
                model="qwen3:4b",
                messages=messages
            )

            print("\nOllama's answer:")
            print(final_response["message"]["content"])


if __name__ == "__main__":
    asyncio.run(main())
