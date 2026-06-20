from pydantic import BaseModel


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "llama3.2"


class ChatResponse(BaseModel):
    reply: str
    model: str


class SummarizeRequest(BaseModel):
    text: str
    model: str = "llama3.2"


class SummarizeResponse(BaseModel):
    summary: str
    model: str


class AskRequest(BaseModel):
    context: str
    question: str
    model: str = "llama3.2"


class AskResponse(BaseModel):
    answer: str
    model: str
