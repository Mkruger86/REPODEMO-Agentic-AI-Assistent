import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from config import configure_openai

configure_openai()

async def main():
    async with MCPServerStreamableHttp(
        name="HTTP Streamable Python MCP Server",
        params={
            "url": "http://localhost:8000/mcp"
        },
    ) as research_server:
        agent = Agent(
            name="Assistant",
            model="gpt-4o",
            instructions="Use the research tools to perform research.",
            mcp_servers=[research_server],
        )

        print("Running: Get the available research sources")

        result = await Runner.run(
            agent,
            "Get the available research sources"
        )

        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())