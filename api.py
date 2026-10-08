import json
import time
import uuid

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict

from config import OPENROUTER_MODEL
from orchestrator import create_plan


app = FastAPI()


class ChatMessage(BaseModel):
    role: str
    content: str

    model_config = ConfigDict(extra="ignore")


class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    stream: bool = False

    model_config = ConfigDict(extra="ignore")


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": OPENROUTER_MODEL,
                "object": "model",
                "owned_by": "agent-backend",
            }
        ],
    }


@app.post("/v1/chat/completions")
async def chat_completions(
    request: ChatCompletionRequest,
):
    if request.model != OPENROUTER_MODEL:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model: {request.model}",
        )

    conversation = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in request.messages
        if message.role in {"user", "assistant"}
    ]

    if not any(
        message["role"] == "user"
        for message in conversation
    ):
        raise HTTPException(
            status_code=400,
            detail="The conversation does not contain a user message.",
        )

    plan = await create_plan(
        messages=conversation,
    )

    content = plan.model_dump_json(
        indent=2,
    )

    completion_id = f"chatcmpl-{uuid.uuid4().hex}"
    created = int(time.time())

    if request.stream:

        async def event_stream():
            content_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": OPENROUTER_MODEL,
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                            "content": content,
                        },
                        "finish_reason": None,
                    }
                ],
            }

            final_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": OPENROUTER_MODEL,
                "choices": [
                    {
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop",
                    }
                ],
            }

            yield f"data: {json.dumps(content_chunk)}\n\n"
            yield f"data: {json.dumps(final_chunk)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
        )

    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": created,
        "model": OPENROUTER_MODEL,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content,
                },
                "finish_reason": "stop",
            }
        ],
    }