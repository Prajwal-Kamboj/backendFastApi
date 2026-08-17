import asyncio
import json
from functools import lru_cache
from pathlib import Path
from typing import Literal

from ddgs import DDGS
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel, Field

import llm_client

SKILL_PATH = Path(__file__).resolve().parent / "skills" / "react-components" / "SKILL.md"


class UIComponent(BaseModel):
    """React component spec for the chat UI."""

    id: Literal["list"] = Field(description='Component id. Use "list" to render a list.')
    title: str = Field(default="", description="Optional heading shown above the list.")
    items: list[str] = Field(description="List items to display. Plain strings only.")


class AgentReply(BaseModel):
    """Final chat reply: prose plus an optional UI component."""

    text: str = Field(description="Plain-text message shown to the user.")
    component: UIComponent | None = Field(
        default=None,
        description='Set when a React component should render. Use id "list" for a list.',
    )


def _clip(text: str, max_len: int = 180) -> str:
    text = " ".join(text.split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def _format_search_hit(hit: dict) -> str:
    title = (hit.get("title") or "").strip()
    body = _clip((hit.get("body") or "").strip())
    href = (hit.get("href") or hit.get("url") or "").strip()
    line = " — ".join(part for part in (title, body) if part) or href
    if href and href not in line:
        line = f"{line} ({href})" if line else href
    return line


def _web_search(query: str, cap: int) -> list:
    return DDGS().text(query, max_results=cap) or []


async def search_results_tool(query: str, limit: int = 10):
    """Search the web for current information matching the query.

    Args:
        query: Search terms to look up on the web
        limit: Maximum number of results to return
    """
    cap = max(1, min(int(limit or 10), 10))
    try:
        hits = await asyncio.wait_for(asyncio.to_thread(_web_search, query, cap), timeout=20)
    except TimeoutError:
        return json.dumps({"error": "Web search timed out. Try a simpler query."})
    except Exception as exc:
        return json.dumps({"error": f"Web search failed: {exc}"})

    items = [
        line
        for hit in hits
        if isinstance(hit, dict) and (line := _format_search_hit(hit))
    ]
    if not items:
        return json.dumps({"error": f"No web results found for {query!r}."})
    return json.dumps(items)


def _skill_prompt() -> str:
    skill = SKILL_PATH.read_text(encoding="utf-8") if SKILL_PATH.exists() else ""
    return (
        "You are a helpful assistant with a web search tool. "
        "Use it whenever the user asks to search, look up, or find current information.\n\n"
        "When the tool returns results, write a short summary in text and render "
        "the hits as a list component. Each list item must be a real title and "
        "snippet from the tool — never invent placeholders like 'record 1'.\n\n"
        "You can create React components in the chat UI. Follow this skill:\n\n"
        f"{skill}"
    )


@lru_cache(maxsize=8)
def get_agent(model: str):
    return create_agent(
        model=llm_client.get_model(model),
        tools=[search_results_tool],
        system_prompt=_skill_prompt(),
        response_format=ToolStrategy(AgentReply),
    )


def _component_payload(structured: AgentReply | None) -> dict | None:
    if structured is None or structured.component is None:
        return None
    data = structured.component.model_dump()
    if data.get("id") == "list" and data.get("items"):
        return data
    return None


async def spawn_agent(messages: list[dict], model: str) -> tuple[str, dict | None]:
    result = await get_agent(model).ainvoke({"messages": messages})
    last = result["messages"][-1]
    structured = result.get("structured_response")
    reply = getattr(structured, "text", None) or llm_client._as_text(last)
    return reply, _component_payload(structured)
