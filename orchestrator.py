from typing import Literal

from agents import Agent, ModelSettings, Runner, function_tool
from pydantic import BaseModel, ConfigDict

from config import orchestrator_model


class OrchestrationTask(BaseModel):
    step: int
    target: Literal["research", "calendar"]
    instruction: str

    model_config = ConfigDict(extra="forbid")


class OrchestrationPlan(BaseModel):
    tasks: list[OrchestrationTask]

    model_config = ConfigDict(extra="forbid")


@function_tool(
    strict_mode=False,
    failure_error_function=None,
)
def submit_plan(
    tasks: list[OrchestrationTask],
) -> str:
    """Submit the completed orchestration plan."""

    plan = OrchestrationPlan(
        tasks=tasks,
    )

    return plan.model_dump_json()


ORCHESTRATOR_INSTRUCTIONS = """
You are the orchestration component of an AI assistant.

Your responsibility is to interpret the user's request and create
an execution plan for the available backend components.

AVAILABLE COMPONENTS

research:
Handles research and information-gathering tasks.
Use this component when the user's request requires finding,
investigating, comparing, or gathering information.

calendar:
Handles calendar, scheduling, availability, and planning tasks.
Use this component when the user's request requires working with
the user's schedule or calendar.

ORCHESTRATION RULES

- Break the request into only the tasks necessary to satisfy it.
- Assign every task to one available component.
- Put tasks in the order in which they must be executed.
- Make each instruction specific enough for the receiving component
  to understand what it must accomplish.
- Do not perform the research yourself.
- Do not perform calendar operations yourself.
- Do not invent backend components that are not listed above.
- Submit the completed execution plan using the submit_plan tool.
"""


orchestrator = Agent(
    name="Orchestrator",
    instructions=ORCHESTRATOR_INSTRUCTIONS,
    model=orchestrator_model,
    tools=[
        submit_plan,
    ],
    tool_use_behavior="stop_on_first_tool",
    model_settings=ModelSettings(
        tool_choice="submit_plan",
        extra_body={
            "provider": {
                "require_parameters": True,
            }
        }
    ),
)


async def create_plan(
    messages: list[dict],
) -> OrchestrationPlan:
    result = await Runner.run(
        orchestrator,
        input=messages,
    )

    return OrchestrationPlan.model_validate_json(
        result.final_output
    )


if __name__ == "__main__":
    user_input = input("User request: ")

    result = Runner.run_sync(
        orchestrator,
        input=user_input,
    )

    plan = OrchestrationPlan.model_validate_json(
        result.final_output
    )

    print(plan)