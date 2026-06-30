import { useState } from 'react'
import { aiApi } from '../api'

const DEFAULT_MODEL = 'llama3.2'

export default function SummarizePanel() {
  const [text, setText] = useState('')
  const [model, setModel] = useState(DEFAULT_MODEL)
  const [summary, setSummary] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSummarize() {
    if (!text.trim() || loading) return
    setSummary(null)
    setError(null)
    setLoading(true)
    try {
      const res = await aiApi.summarize({ text, model })
      setSummary(res.summary)
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
        <label className="field-label">Text to summarize</label>
        <textarea
          className="big-textarea"
          rows={8}
          placeholder="Paste or type the text you want summarized…"
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={loading}
        />
      </div>

      <button
        className="btn btn-primary"
        onClick={handleSummarize}
        disabled={loading || !text.trim()}
      >
        {loading ? 'Summarizing…' : 'Summarize'}
      </button>

      {error && <p className="error-msg">{error}</p>}

      {summary && (
        <div className="result-box">
          <span className="result-label">Summary</span>
          <pre className="result-text">{summary}</pre>
        </div>
      )}
    </div>
  )
}
