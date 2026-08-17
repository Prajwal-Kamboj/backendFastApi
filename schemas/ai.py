from pydantic import BaseModel


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]
    model: str = "gemini-3.6-flash"
    agent_mode: bool = False


class UIComponent(BaseModel):
    id: str  # "list" for now
    title: str | None = None
    items: list[str] = []


class ChatResponse(BaseModel):
    reply: str
    model: str
    component: UIComponent | None = None


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
