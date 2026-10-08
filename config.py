import os

from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled


# We are using OpenRouter rather than an OpenAI API key.
# OpenAI tracing therefore gets disabled for this prototype.
set_tracing_disabled(True)


openrouter_client = AsyncOpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)


orchestrator_model = OpenAIChatCompletionsModel(
    model="openrouter/free",
    openai_client=openrouter_client,
)
