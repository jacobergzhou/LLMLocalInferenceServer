from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
import asyncio

from app.models import ChatRequest

app = FastAPI()

@app.get("/health_check")
async def health_check():
    return JSONResponse({"status": "ok"})

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    last_user_message = ""
    for m in reversed(req.messages):
        if m.role == "user":
            last_user_message = m.content
            break
    return {
        "model": req.model,
        "reply": f"Echo: {last_user_message}",
        "used_max_tokens": req.max_tokens,
        "temperature": req.temperature,
        "stream": req.stream
    }

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