import httpx

OLLAMA_BASE_URL = "http://localhost:11434"


async def chat(messages: list[dict], model: str) -> str:
    """Send a multi-turn chat to Ollama and return the reply text."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": model,
                "messages": messages,
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]


async def generate(prompt: str, model: str) -> str:
    """Send a single prompt to Ollama and return the generated text."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["response"]
