from typing import Literal, List
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: Literal['user', 'assistant', 'system']
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(2048, gt=0)
    stream: bool = True