import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(false)

  const askQuestion = async () => {
    if (!question.trim()) return
    setLoading(true)
    setAnswer('')
    setSources([])

    try {
      const response = await fetch('https://echome-backend-0gzm.onrender.com/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      })
      const data = await response.json()
      setAnswer(data.answer)
      setSources(data.sources)
    } catch (err) {
      setAnswer('Something went wrong. Make sure the backend server is running.')
    }

    setLoading(false)
  }

  return (
    <div className="app-container">
<div className="header-block">
  <h1>EchoMe</h1>
  <p className="subtitle">Ask a question, get an answer based on my real thoughts and opinions</p>
</div>

      <div className="input-row">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && askQuestion()}
          placeholder="e.g. How do you feel about mornings?"
        />
        <button onClick={askQuestion} disabled={loading}>
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </div>

      {answer && (
        <div className="answer-box">
          <h3>Answer</h3>
          <p>{answer}</p>
        </div>
      )}

      {sources.length > 0 && (
        <div className="sources-box">
          <h3>Based on these past entries</h3>
          <ul>
            {sources.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App