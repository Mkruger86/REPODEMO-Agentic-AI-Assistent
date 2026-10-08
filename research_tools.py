import asyncio
import json

from ddgs import DDGS
from ddgs.exceptions import DDGSException
from langchain.tools import tool


@tool
async def web_search(query: str) -> str:
    """Search the public web for information relevant to a research task."""

    query = query.strip()

    if not query:
        return json.dumps(
            {
                "error": "The search query was empty."
            }
        )

    try:
        results = await asyncio.to_thread(
            DDGS(timeout=10).text,
            query,
            max_results=5,
            safesearch="moderate",
        )
    except DDGSException:
        return json.dumps(
            {
                "error": "Web search is temporarily unavailable."
            }
        )

    normalized_results = [
        {
            "title": result.get("title", ""),
            "url": result.get("href", ""),
            "snippet": result.get("body", ""),
        }
        for result in results
    ]

    return json.dumps(
        normalized_results,
        ensure_ascii=False,
    )