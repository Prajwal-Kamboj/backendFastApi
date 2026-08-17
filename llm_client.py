import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv(Path(__file__).resolve().parent / ".env")

DEFAULT_MODEL = "gemini-3.6-flash"


@lru_cache(maxsize=8)
def get_model(model: str):
    """Return a chat model. Bare names are treated as Google Gemini."""
    if not (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")):
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Add it to the environment or a .env file in the project root."
        )
    if ":" not in model:
        model = f"google_genai:{model}"
    return init_chat_model(model)


def _as_text(message) -> str:
    """Return plain text from a LangChain message or raw content blocks."""
    text = getattr(message, "text", None)
    if isinstance(text, str) and text:
        return text
    content = getattr(message, "content", message)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and isinstance(block.get("text"), str):
                parts.append(block["text"])
        joined = "".join(parts)
        if joined:
            return joined
    return str(content)


async def chat(messages: list[dict], model: str) -> str:
    """Send a multi-turn chat and return the reply text."""
    result = await get_model(model).ainvoke(messages)
    return _as_text(result)


async def generate(prompt: str, model: str) -> str:
    """Send a single prompt and return the generated text."""
    result = await get_model(model).ainvoke(prompt)
    return _as_text(result)
