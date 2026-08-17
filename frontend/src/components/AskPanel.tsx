import { useState } from 'react'
import { aiApi } from '../api'

const DEFAULT_MODEL = 'gemini-3.6-flash'

export default function AskPanel() {
  const [context, setContext] = useState('')
  const [question, setQuestion] = useState('')
  const [model, setModel] = useState(DEFAULT_MODEL)
  const [answer, setAnswer] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleAsk() {
    if (!context.trim() || !question.trim() || loading) return
    setAnswer(null)
    setError(null)
    setLoading(true)
    try {
      const res = await aiApi.ask({ context, question, model })
      setAnswer(res.answer)
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Unknown error')
    } finally {
      setLoading(false)
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
      </div>

      <div className="field-group">
        <label className="field-label">Context</label>
        <textarea
          className="big-textarea"
          rows={6}
          placeholder="Provide the background text / document the model should use…"
          value={context}
          onChange={(e) => setContext(e.target.value)}
          disabled={loading}
        />
      </div>

      <div className="field-group">
        <label className="field-label">Question</label>
        <input
          className="question-input"
          type="text"
          placeholder="Ask something about the context above…"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          disabled={loading}
          onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
        />
      </div>

      <button
        className="btn btn-primary"
        onClick={handleAsk}
        disabled={loading || !context.trim() || !question.trim()}
      >
        {loading ? 'Thinking…' : 'Ask'}
      </button>

      {error && <p className="error-msg">{error}</p>}

      {answer && (
        <div className="result-box">
          <span className="result-label">Answer</span>
          <pre className="result-text">{answer}</pre>
        </div>
      )}
    </div>
  )
}
