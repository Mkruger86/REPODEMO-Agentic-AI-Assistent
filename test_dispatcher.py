import asyncio

from dispatcher import Dispatcher
from orchestrator import (
    OrchestrationPlan,
    OrchestrationTask,
)


async def research_test_handler(
    instruction: str,
) -> str:
    return f"Research received: {instruction}"


async def calendar_test_handler(
    instruction: str,
) -> str:
    return f"Calendar received: {instruction}"


async def main() -> None:
    dispatcher = Dispatcher(
        handlers={
            "research": research_test_handler,
            "calendar": calendar_test_handler,
        }
    )

    plan = OrchestrationPlan(
        tasks=[
            OrchestrationTask(
                step=2,
                target="calendar",
                instruction="Check tomorrow's availability.",
            ),
            OrchestrationTask(
                step=1,
                target="research",
                instruction="Research AI security risks.",
            ),
        ]
    )

    results = await dispatcher.dispatch(plan)

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())