from fastapi import APIRouter, HTTPException

import ollama_client
from schemas.ai import (
    AskRequest,
    AskResponse,
    ChatRequest,
    ChatResponse,
    SummarizeRequest,
    SummarizeResponse,
)

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Multi-turn conversation with the model."""
    try:
        messages = [m.model_dump() for m in request.messages]
        reply = await ollama_client.chat(messages, request.model)
        return ChatResponse(reply=reply, model=request.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    """Summarize a block of text."""
    try:
        prompt = f"Summarize the following text concisely:\n\n{request.text}"
        summary = await ollama_client.generate(prompt, request.model)
        return SummarizeResponse(summary=summary, model=request.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    """Answer a question based on a given context."""
    try:
        prompt = (
            f"Use the following context to answer the question.\n\n"
            f"Context:\n{request.context}\n\n"
            f"Question: {request.question}\n\n"
            f"Answer:"
        )
        answer = await ollama_client.generate(prompt, request.model)
        return AskResponse(answer=answer, model=request.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
