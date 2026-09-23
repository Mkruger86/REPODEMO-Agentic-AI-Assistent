import asyncio
from pathlib import Path

from agents import Agent, Runner
from agents.mcp import MCPServerStdio, MCPServerStdioParams
from config import configure_openai

configure_openai()

SCRIPT = Path(__file__).with_name("Claude_MCP_Server.py").resolve()


async def main():
    async with MCPServerStdio(
        name="Research Tools",
        params=MCPServerStdioParams(
            command="mcp",
            args=["run", str(SCRIPT)]
        ),
     ) as research_server:
        agent = Agent(
            name="Assistant",
            model="gpt-4o",
            instructions="Use the research tools to perform research.",
            mcp_servers=[research_server],
        )

        print("Running: Get the available research sources")
        result = await Runner.run(agent, "Get the available research sources")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())