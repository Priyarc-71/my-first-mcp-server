
import asyncio
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("My First MCP Server")


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Please enter whole numbers.")
    return a + b


@mcp.tool()
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Please enter whole numbers.")
    return a * b


@mcp.resource("info://project")
def project_info() -> str:
    """Provide information about this project."""
    return "This MCP server provides addition and multiplication tools."


@mcp.prompt()
def math_helper(operation: str) -> str:
    """Help the user with a math operation."""
    return f"Help the user with this math operation: {operation}. Explain the answer simply."


async def main():
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
