from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from orchestrator import OrchestrationPlan


TaskHandler = Callable[[str], Awaitable[str]]


@dataclass(frozen=True, slots=True)
class TaskResult:
    step: int
    target: str
    output: str


class Dispatcher:
    def __init__(
        self,
        handlers: dict[str, TaskHandler],
    ) -> None:
        self._handlers = handlers.copy()

    async def dispatch(
        self,
        plan: OrchestrationPlan,
    ) -> list[TaskResult]:
        if not plan.tasks:
            raise ValueError(
                "The orchestration plan contains no tasks."
            )

        ordered_tasks = sorted(
            plan.tasks,
            key=lambda task: task.step,
        )

        seen_steps: set[int] = set()
        results: list[TaskResult] = []

        for task in ordered_tasks:
            if task.step in seen_steps:
                raise ValueError(
                    f"Duplicate orchestration step: {task.step}"
                )

            seen_steps.add(task.step)

            handler = self._handlers.get(task.target)

            if handler is None:
                raise RuntimeError(
                    f"No handler registered for target '{task.target}'."
                )

            output = await handler(
                task.instruction
            )

            if not isinstance(output, str):
                raise TypeError(
                    f"Handler for '{task.target}' returned a non-string result."
                )

            results.append(
                TaskResult(
                    step=task.step,
                    target=task.target,
                    output=output,
                )
            )

        return results