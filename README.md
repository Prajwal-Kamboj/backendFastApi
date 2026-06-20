<div align="center">

# Structured AI · Widget Engine

**Ollama responses → JSON schema → Interactive UI components**

*A FastAPI backend that turns raw LLM output into structured data contracts, powering a layer of interactive, composable, and fully customizable UI widgets.*

[![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Ollama](https://img.shields.io/badge/Ollama-local%20LLM-black?style=flat-square)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

</div>

---

## The Core Idea

Most AI integrations pipe raw text into a `<p>` tag. This project does the opposite.

Every response from the Ollama model is **forced into a typed JSON contract**. The frontend reads that contract and decides which widget to render — not what text to display.

```
User prompt
    │
    ▼
FastAPI endpoint  →  Ollama (local LLM)  →  structured JSON response
                                                      │
                              ┌───────────────────────┤
                              ▼                       ▼
                        widget: "chart"         widget: "comparison"
                        data: [...]             items: [...]
                              │                       │
                              ▼                       ▼
                     <BarChartWidget />      <ComparisonCardWidget />
```

The LLM never owns the UI. The schema does.

---

## Why This Architecture

| Approach | Output | Problem |
|---|---|---|
| Raw LLM text | `"The answer is 42..."` | Unparseable, unrenderable |
| Markdown streaming | `## Answer\n**42**` | Still just styled text |
| **This project** | `{ widget: "stat", value: 42 }` | **Renderable, interactive, composable** |

Forcing the model to output a schema means every response is a *UI instruction*, not a sentence.

---

## Widget Types

Each endpoint returns a `widget` field that maps to a frontend component. The schema defines exactly what that component needs.

<details>
<summary><strong>Stat Card</strong> — a single highlighted metric</summary>

```json
{
  "widget": "stat",
  "label": "Estimated Reading Time",
  "value": "4 min",
  "trend": "+12% vs last week",
  "color": "blue"
}
```

Renders as a glanceable card with an animated value and optional trend indicator.

</details>

<details>
<summary><strong>Comparison Table</strong> — side-by-side structured data</summary>

```json
{
  "widget": "comparison",
  "title": "Python vs JavaScript",
  "columns": ["Feature", "Python", "JavaScript"],
  "rows": [
    ["Typing", "Optional static", "Optional static"],
    ["Runtime", "CPython", "V8 / Node"],
    ["Best for", "Data / ML / APIs", "Browser / Full-stack"]
  ],
  "highlight_col": 1
}
```

Renders as a sortable, highlighted table — not a markdown block.

</details>

<details>
<summary><strong>Step List</strong> — sequential instructions with state</summary>

```json
{
  "widget": "steps",
  "title": "How to set up Ollama",
  "steps": [
    { "label": "Install Ollama", "command": "brew install ollama" },
    { "label": "Pull a model", "command": "ollama pull llama3.2" },
    { "label": "Start the server", "command": "ollama serve" }
  ]
}
```

Renders as interactive checklist steps — each one clickable, copyable, and stateful.

</details>

<details>
<summary><strong>Chart</strong> — data the model returns, visualized instantly</summary>

```json
{
  "widget": "bar_chart",
  "title": "Language Popularity 2024",
  "x_label": "Language",
  "y_label": "Usage %",
  "data": [
    { "label": "Python", "value": 28.3 },
    { "label": "JavaScript", "value": 25.1 },
    { "label": "Rust", "value": 13.7 }
  ]
}
```

Renders as an animated bar chart — not a table, not a list.

</details>

<details>
<summary><strong>Decision Tree</strong> — branching logic the user can explore</summary>

```json
{
  "widget": "decision",
  "question": "What type of database should I use?",
  "branches": [
    {
      "label": "Need relations?",
      "yes": { "widget": "stat", "label": "Use", "value": "PostgreSQL" },
      "no": {
        "label": "Need scale > 10M docs?",
        "yes": { "widget": "stat", "label": "Use", "value": "Cassandra" },
        "no": { "widget": "stat", "label": "Use", "value": "MongoDB" }
      }
    }
  ]
}
```

Renders as an interactive branching explorer — click through the logic.

</details>

---

## API Endpoints

### `POST /chat`

General multi-turn conversation. Returns a widget schema based on the nature of the reply.

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{ "role": "user", "content": "Compare REST vs GraphQL" }],
    "model": "llama3.2"
  }'
```

```json
{
  "widget": "comparison",
  "title": "REST vs GraphQL",
  "columns": ["Aspect", "REST", "GraphQL"],
  "rows": [...]
}
```

---

### `POST /summarize`

Summarizes text and returns it as a structured stat or highlight widget.

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{ "text": "...", "model": "llama3.2" }'
```

---

### `POST /ask`

Answers a question using a given context block. Returns a focused answer widget.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "context": "FastAPI is a modern Python framework...",
    "question": "What makes FastAPI fast?",
    "model": "llama3.2"
  }'
```

---

## Stack

| Layer | Technology | Role |
|---|---|---|
| **API** | FastAPI + Uvicorn | Routes, validation, async handling |
| **LLM** | Ollama (local) | Inference — no API keys, no cost |
| **Schemas** | Pydantic | Typed request/response contracts |
| **HTTP Client** | httpx | Async calls to Ollama's REST API |
| **Widget Layer** | JSON schema | LLM output → UI instructions |

---

## Project Structure

```
backendFastApi/
├── main.py              # FastAPI app — all 3 endpoints
├── ollama_client.py     # Async wrapper around Ollama's REST API
├── models.py            # Pydantic schemas: request + response types
├── widget_schema.py     # JSON contracts for every widget type
├── pyproject.toml       # Project metadata
└── .venv/               # Isolated Python environment
```

---

## Getting Started

**1. Install Ollama and pull a model**

```bash
# macOS
brew install ollama
ollama pull llama3.2
ollama serve
```

**2. Clone and activate the environment**

```bash
git clone https://github.com/your-username/backendFastApi.git
cd backendFastApi
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate  # macOS / Linux
```

**3. Install dependencies**

```bash
pip install fastapi uvicorn httpx pydantic python-dotenv
```

**4. Run the server**

```bash
uvicorn main:app --reload
```

Open [`http://localhost:8000/docs`](http://localhost:8000/docs) for the interactive Swagger UI.

---

## Design Principles

**Schema-first, not text-first.**
The system prompt instructs the model to always respond in a specific JSON format. The `widget` field is required. If the model drifts, the backend rejects the response.

**Widgets are composable.**
A `decision` widget can nest `stat` widgets. A `steps` widget can contain `chart` widgets. The schema is recursive by design.

**Widgets are customizable.**
Every widget schema includes optional `color`, `variant`, and `theme` fields. The frontend adapts without a code change.

**Local-first.**
No OpenAI key. No cloud spend. No rate limits. Ollama runs on your machine — inference is free and private.

---

<div align="center">

*Built as a portfolio project — demonstrating that LLM output doesn't have to be text.*

</div>
