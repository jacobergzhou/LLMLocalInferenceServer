import time
import uuid
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio

from app.models import ChatRequest, ChatResponse, Choice, Message, Usage

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health_check")
async def health_check():
    return JSONResponse({"status": "ok"})

@app.post("/chat")
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    # 1. very naive "toy" completion
    user_message = request.messages[-1].content if request.messages else ""
    completion_text = f"Echo: {user_message}"

    # 2. fake token counting (later: count properly)
    prompt_tokens = len(user_message.split())
    completion_tokens = len(completion_text.split())
    total_tokens = prompt_tokens + completion_tokens

    # 3. build response
    now = int(time.time())
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"

    choice = Choice(
        index=0,
        message=Message(role="assistant", content=completion_text),
        finish_reason="stop",
    )

    usage = Usage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
    )

    return ChatResponse(
        id=completion_id,
        created=now,
        model=request.model,
        choices=[choice],
        usage=usage,
    )


@app.websocket("/websocket")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            message = await ws.receive_text()
            try:
                req = ChatRequest.model_validate_json(message)
            except Exception:
                await ws.send_text(f"Invalid request format {message}")
                continue
            last_user_msg = ""
            for m in reversed(req.messages):
                if m.role == "user":
                    last_user_msg = m.content
                    break
            await ws.send_text(f"Received message: {last_user_msg}")
    except Exception:
        await ws.close()

@app.websocket("/websocket/stream")
async def ws_stream(ws: WebSocket):
    await ws.accept()
    tokens = ["This", "is", "a", "test", "streaming"]
    try:
        for t in tokens:
            await ws.send_text(t)
            await asyncio.sleep(1.0)
    except Exception:
        await ws.close()
