import asyncio
from dataclasses import dataclass, field
from typing import AsyncIterator, Dict, List, Optional

from app.model.toy_model import generate_tokens

@dataclass(eq=False)
class GenerationRequest:
    prompt: str
    out_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    done: asyncio.Event = field(default_factory=asyncio.Event)

class Batcher:
    """
    Collects incoming requests into small batches, then interleaves token
    generation round-robin across the batch to simulate a real LLM scheduler.
    """
    def __init__(self, max_batch_size = 8, collect_ms: int = 50, tick_ms: int = 25):
        self._in: asyncio.Queue[GenerationRequest] = asyncio.Queue()
        self.max_batch_size = max_batch_size
        self.collect_ms = collect_ms
        self.tick_ms = tick_ms

    async def submit(self, req: GenerationRequest) -> None:
        await self._in.put(req)

    async def process_forever(self) -> None:
        while True:
            req = await self._in.get()
            batch: List[GenerationRequest] = [req]

            # Short collection window to form a batch
            try: 
                while len(batch) < self.max_batch_size:
                    nxt = await asyncio.wait_for(self._in.get(), timeout = self.collect_ms/1000)
                    batch.append(nxt)
            except asyncio.TimeoutError:
                pass

            # Create async generators for this batch
            gens: Dict[GenerationRequest, AsyncIterator[str]] = {
                r: generate_tokens(r.prompt) for r in batch
            }

            alive = set(gens)

            while alive:
                for r in list(alive):
                    gen = gens[r]
                    try:
                        tok = await gen.__anext__()
                        await r.out_queue.put(tok)
                    except StopAsyncIteration:
                        await r.out_queue.put("[DONE]")
                        r.done.set()
                        alive.remove(r)
                await asyncio.sleep(self.tick_ms/1000)