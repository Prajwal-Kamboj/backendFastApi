from pydantic import BaseModel


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "gemini-3.6-flash"
    agent_mode: bool = False


class ChatResponse(BaseModel):
    reply: str
    model: str


class SummarizeRequest(BaseModel):
    text: str
    model: str = "gemini-3.6-flash"


class SummarizeResponse(BaseModel):
    summary: str
    model: str


class AskRequest(BaseModel):
    context: str
    question: str
    model: str = "gemini-3.6-flash"


class AskResponse(BaseModel):
    answer: str
    model: str
