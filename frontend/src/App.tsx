import { useState } from 'react'
import ChatPanel from './components/ChatPanel'
import SummarizePanel from './components/SummarizePanel'
import AskPanel from './components/AskPanel'
import './App.css'

type Tab = 'chat' | 'summarize' | 'ask'

const TABS: { id: Tab; label: string; icon: string }[] = [
  { id: 'chat', label: 'Chat', icon: '💬' },
  { id: 'summarize', label: 'Summarize', icon: '📝' },
  { id: 'ask', label: 'Ask', icon: '🔍' },
]

export default function App() {
  const [tab, setTab] = useState<Tab>('chat')

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-logo">
          <span className="logo-icon">⚡</span>
          <span className="logo-text">Gemini UI</span>
        </div>
        <nav className="tab-nav">
          {TABS.map((t) => (
            <button
              key={t.id}
              className={`tab-btn ${tab === t.id ? 'tab-btn--active' : ''}`}
              onClick={() => setTab(t.id)}
            >
              <span>{t.icon}</span>
              <span>{t.label}</span>
            </button>
          ))}
        </nav>
      </header>

      <main className="app-main">
        {tab === 'chat' && <ChatPanel />}
        {tab === 'summarize' && <SummarizePanel />}
        {tab === 'ask' && <AskPanel />}
      </main>
    </div>
  )
}
