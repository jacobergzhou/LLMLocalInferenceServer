import re
import asyncio
from typing import AsyncIterator

TOKEN_RE = re.compile(r"\w+|[^\w\s]|\s+")

def simple_tokenize(text: str):
    # Yields words, punctuation, and whitespace as separate "tokens"
    return TOKEN_RE.findall(text)


async def generate_tokens(prompt: str, delay_ms: int = 60) -> AsyncIterator[str]:
    """
    A tiny async generator that "completes" by echoing your prompt
    and a canned suffix, token by token.
    """
    suffix = "This is a tiny streaming demo using a toy tokenizer."
    text = f"Echo: {prompt} | {suffix}"
    for tok in simple_tokenize(text):
        await asyncio.sleep(delay_ms / 1000)
        yield tok