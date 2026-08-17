import json
from functools import lru_cache
from pathlib import Path
from typing import Literal

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


def search_results_tool(query: str, limit: int = 10):
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    cap = max(1, min(limit, 10))
    records = [f"{query} — record {i}" for i in range(1, cap + 1)]
    return json.dumps(records)


def _skill_prompt() -> str:
    skill = SKILL_PATH.read_text(encoding="utf-8") if SKILL_PATH.exists() else ""
    return (
        "You are a helpful assistant with access to a customer database "
        "search tool. Use it when the user asks to look up records.\n\n"
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
