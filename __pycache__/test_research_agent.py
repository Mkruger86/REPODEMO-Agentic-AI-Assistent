import asyncio

from research_agent import research_agent


async def main() -> None:
    result = await research_agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Research the current LangChain Python agent API. "
                        "Explain what create_agent does and include sources."
                    ),
                }
            ]
        }
    )

    for message in result["messages"]:
        print(
            type(message).__name__,
            message.text,
        )


if __name__ == "__main__":
    asyncio.run(main())