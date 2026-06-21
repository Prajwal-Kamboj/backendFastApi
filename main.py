import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middlewares import RequestLoggingMiddleware
from routers import ai_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)

app = FastAPI(title="AI API", description="Local AI API powered by Ollama")

# ── Middlewares ────────────────────────────────────────────────────────────────
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(ai_router)


@app.get("/")
async def root():
    return {"status": "running", "docs": "/docs"}
