from functools import lru_cache

from langchain.agents import create_agent

import llm_client


def search_results_tool(query: str, limit: int = 10):
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"


@lru_cache(maxsize=8)
def get_agent(model: str):
    return create_agent(
        model=llm_client.get_model(model),
        tools=[search_results_tool],
        system_prompt=(
            "You are a helpful assistant with access to a customer database "
            "search tool. Use it when the user asks to look up records."
        ),
    )


async def spawn_agent(messages: list[dict], model: str) -> str:
    result = await get_agent(model).ainvoke({"messages": messages})
    last = result["messages"][-1]
    return llm_client._as_text(last)
