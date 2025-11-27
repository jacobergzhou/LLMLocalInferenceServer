from typing import Literal, List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ---- Messages ----
class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    # optional: future-proof for function/tool calls or named roles (like "assistant:name")
    name: Optional[str] = None


# ---- Request ----
class ChatRequest(BaseModel):
    model: str
    messages: List[Message]

    # sampling controls
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    top_p: float = Field(1.0, ge=0.0, le=1.0)

    # output size & how many completions
    max_tokens: int = Field(256, gt=0)
    n: int = Field(1, ge=1, le=4)

    # streaming vs non-streaming
    stream: bool = False

    # stopping conditions
    stop: Optional[List[str]] = None

    # observability / abuse tracing
    user: Optional[str] = None

    # free-form metadata (for logging, routing decisions, etc.)
    metadata: Optional[Dict[str, Any]] = None


# ---- Response ----


class Choice(BaseModel):
    index: int
    message: Message
    finish_reason: Optional[Literal["stop", "length", "error"]] = None


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    id: str                           # e.g. "chatcmpl-123"
    object: str = "chat.completion"   # matches OpenAI style
    created: int                      # unix timestamp
    model: str                        # echo back request.model
    choices: List[Choice]
    usage: Usage

