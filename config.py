import os

from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled


OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

OPENROUTER_MODEL = "apodex/apodex-1.1-mini:free"


set_tracing_disabled(True)


openrouter_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    timeout=30.0,
    max_retries=0,
)


orchestrator_model = OpenAIChatCompletionsModel(
    model=OPENROUTER_MODEL,
    openai_client=openrouter_client,
)