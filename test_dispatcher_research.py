import asyncio

from dispatcher import Dispatcher
from orchestrator import OrchestrationPlan, OrchestrationTask
from research_agent import run_research


async def main() -> None:
    dispatcher = Dispatcher(
        handlers={
            "research": run_research,
        }
    )

    plan = OrchestrationPlan(
        tasks=[
            OrchestrationTask(
                step=1,
                target="research",
                instruction=(
                    "Research the current LangChain Python agent API. "
                    "Explain what create_agent does and include sources."
                ),
            )
        ]
    )

    results = await dispatcher.dispatch(plan)

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(main())