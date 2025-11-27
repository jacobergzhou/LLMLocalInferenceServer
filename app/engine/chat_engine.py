# engine/chat_engine.py
import asyncio

async def run_toy_llm(prompt: str) -> str:
    await asyncio.sleep(0.3)  # simulate model latency
    return f"Echo: {prompt}"
