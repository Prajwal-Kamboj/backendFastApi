const BASE = '/api'

// ── Types ──────────────────────────────────────────────────────────────────

export interface UIComponent {
  id: 'list' | string
  title?: string | null
  items: string[]
}

export interface Message {
  role: 'user' | 'assistant'
  content: string
  component?: UIComponent | null
}

export interface ChatRequest {
  messages: Message[]
  model?: string
  agent_mode?: boolean
}

export interface ChatResponse {
  reply: string
  model: string
  component?: UIComponent | null
}

export interface SummarizeRequest {
  text: string
  model?: string
}

export interface SummarizeResponse {
  summary: string
  model: string
}

export interface AskRequest {
  context: string
  question: string
  model?: string
}

export interface AskResponse {
  answer: string
  model: string
}

// ── Helpers ────────────────────────────────────────────────────────────────

async function post<TReq, TRes>(path: string, body: TReq): Promise<TRes> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? 'Request failed')
  }
  return res.json() as Promise<TRes>
}

// ── Endpoints ──────────────────────────────────────────────────────────────

export const aiApi = {
  chat: (req: ChatRequest) =>
    post<ChatRequest, ChatResponse>('/ai/chat', req),

  summarize: (req: SummarizeRequest) =>
    post<SummarizeRequest, SummarizeResponse>('/ai/summarize', req),

  ask: (req: AskRequest) =>
    post<AskRequest, AskResponse>('/ai/ask', req),
}
