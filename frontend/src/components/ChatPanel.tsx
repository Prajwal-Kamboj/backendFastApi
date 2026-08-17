import { useState, useRef, useEffect } from 'react'
import { aiApi } from '../api'
import type { Message, UIComponent } from '../api'

function ResultList({ component }: { component: UIComponent }) {
  return (
    <div className="result-list">
      {component.title && <h3 className="result-list-title">{component.title}</h3>}
      <ol className="result-list-items">
        {component.items.map((item, i) => (
          <li key={i} className="result-list-item">
            <span className="result-list-index">{i + 1}</span>
            <span className="result-list-label">{item}</span>
          </li>
        ))}
      </ol>
    </div>
  )
}

const DEFAULT_MODEL = 'gemini-3.6-flash'

export default function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [model, setModel] = useState(DEFAULT_MODEL)
  const [agentMode, setAgentMode] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function send() {
    const text = input.trim()
    if (!text || loading) return

    const next: Message[] = [...messages, { role: 'user', content: text }]
    setMessages(next)
    setInput('')
    setError(null)
    setLoading(true)

    try {
      const payload = next.map(({ role, content }) => ({ role, content }))
      const { reply, component } = await aiApi.chat({
        messages: payload,
        model,
        agent_mode: agentMode,
      })
      setMessages([...next, { role: 'assistant', content: reply, component }])
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }
  

  return (
    <div className="panel">
      <div className="panel-toolbar">
        <label>
          Model
          <input
            className="model-input"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          />
        </label>
        <label className="toggle">
          <input
            type="checkbox"
            checked={agentMode}
            onChange={(e) => setAgentMode(e.target.checked)}
          />
          Agent mode
        </label>
        <button
          className="btn btn-ghost"
          onClick={() => { setMessages([]); setError(null) }}
          disabled={messages.length === 0}
        >
          Clear
        </button>
      </div>

      <div className="messages">
        {messages.length === 0 && (
          <p className="placeholder">Start a conversation below…</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`bubble bubble-${m.role}`}>
            <span className="bubble-label">{m.role === 'user' ? 'You' : agentMode ? 'Agent' : 'AI'}</span>
            {m.content && <pre className="bubble-text">{m.content}</pre>}
            {m.role === 'assistant' && m.component?.id === 'list' && m.component.items.length > 0 && (
              <ResultList component={m.component} />
            )}
          </div>
        ))}
        {loading && (
          <div className="bubble bubble-assistant">
            <span className="bubble-label">{agentMode ? 'Agent' : 'AI'}</span>
            <span className="typing-dots"><span /><span /><span /></span>
          </div>
        )}
        {error && <p className="error-msg">{error}</p>}
        <div ref={bottomRef} />
      </div>

      <div className="input-row">
        <textarea
          className="chat-input"
          rows={3}
          placeholder={
            agentMode
              ? 'Search the web for LangChain agents and return 5 results.'
              : 'Type a message… (Enter to send, Shift+Enter for newline)'
          }
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />
        <button className="btn btn-primary" onClick={send} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  )
}
