import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ToolResult,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Server("my-mcp-server")


HELLO_TOOL = Tool(
    name="hello",
    description="Greets a person with their name",
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the person to greet",
            }
        },
        "required": ["name"],
    },
)


ADD_TOOL = Tool(
    name="add",
    description="Adds two numbers together",
    inputSchema={
        "type": "object",
        "properties": {
            "a": {
                "type": "number",
                "description": "First number",
            },
            "b": {
                "type": "number",
                "description": "Second number",
            },
        },
        "required": ["a", "b"],
    },
)





@server.call_tool()
async def handle_tool_call(name: str, arguments: dict) -> ToolResult:

    logger.info(f"Tool called: {name} with arguments: {arguments}")

    if name == "hello":
        person_name = arguments.get("name", "World")
        result = f"Hello, {person_name}! 👋"
        return ToolResult(content=[TextContent(type="text", text=result)])

    elif name == "add":
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        result = a + b
        return ToolResult(
            content=[TextContent(type="text", text=f"{a} + {b} = {result}")]
        )

    else:
        return ToolResult(
            content=[TextContent(type="text", text=f"Unknown tool: {name}")],
            isError=True,
        )



@server.list_tools()
async def list_tools() -> list[Tool]:
    return [HELLO_TOOL, ADD_TOOL]



async def main():

    from mcp.server.stdio import stdio_server

    async with stdio_server() as streams:
        await server.run(
            streams.input,
            streams.output,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())