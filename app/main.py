from fastapi import FastAPI, WebSocket;
from fastapi.responses import JSONResponse;
import asyncio;

app = FastAPI()

@app.get("/health_check")
async def health_check():
    return JSONResponse({"status": "ok"})

@app.websocket("/websocket")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            message = await ws.receive_text()
            await ws.send_text(f"Received message: {message}")
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