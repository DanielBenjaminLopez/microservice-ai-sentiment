import { useState } from 'react'
import './App.css'

function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const analyzeSentiment = async () => {
    if (!text.trim()) {
      setError('Por favor ingresa un texto')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`/api/analyze/?text=${encodeURIComponent(text)}`)
      if (!response.ok) {
        throw new Error('Error al conectar con la API')
      }
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Error: ' + err.message)
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      analyzeSentiment()
    }
  }

  const getEmoji = (label) => {
    switch(label) {
      case 'positivo':
        return '😊'
      case 'negativo':
        return '😢'
      case 'neutral':
        return '😐'
      default:
        return '❓'
    }
  }

  const getColor = (label) => {
    switch(label) {
      case 'positivo':
        return '#10B981'
      case 'negativo':
        return '#EF4444'
      case 'neutral':
        return '#6B7280'
      default:
        return '#9CA3AF'
    }
  }

  const getLabel = (label) => {
    switch(label) {
      case 'positivo':
        return 'Positivo ✨'
      case 'negativo':
        return 'Negativo 💔'
      case 'neutral':
        return 'Neutral 🤷'
      default:
        return 'Desconocido'
    }
  }

  return (
    <div className="app-container">
      <div className="gradient-bg"></div>
      
      <div className="content">
        <header className="header">
          <div className="title-section">
            <h1>✨ Analizador de Sentimiento</h1>
            <p className="subtitle">Descubre el sentimiento detrás de tus palabras</p>
          </div>
        </header>

        <main className="main">
          <div className="card input-card">
            <label htmlFor="text-input" className="label">¿Qué quieres analizar?</label>
            <textarea
              id="text-input"
              className="textarea"
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Escribe un texto aquí... (Presiona Shift+Enter para salto de línea)"
              rows="5"
            />
            <button
              className={`analyze-btn ${loading ? 'loading' : ''}`}
              onClick={analyzeSentiment}
              disabled={loading}
            >
              {loading ? (
                <span className="spinner">⟳</span>
              ) : (
                'Analizar Sentimiento'
              )}
            </button>
          </div>

          {error && (
            <div className="card error-card">
              <p className="error-text">⚠️ {error}</p>
            </div>
          )}

          {result && (
            <div className="card result-card">
              <div className="result-content">
                <div className="result-emoji">{getEmoji(result.label)}</div>
                <div className="result-info">
                  <p className="result-label">Sentimiento Detectado:</p>
                  <h2 
                    className="result-value"
                    style={{ color: getColor(result.label) }}
                  >
                    {getLabel(result.label)}
                  </h2>
                  <div className="result-text">
                    <p><strong>Texto analizado:</strong></p>
                    <p className="text-preview">{text}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div className="info-cards">
            <div className="mini-card positive">
              <span className="mini-emoji">😊</span>
              <p><strong>Positivo:</strong> Expresa sentimientos alegres y optimistas</p>
            </div>
            <div className="mini-card negative">
              <span className="mini-emoji">😢</span>
              <p><strong>Negativo:</strong> Expresa sentimientos tristes o pesimistas</p>
            </div>
            <div className="mini-card neutral">
              <span className="mini-emoji">😐</span>
              <p><strong>Neutral:</strong> Sin sentimiento claro o ambiguo</p>
            </div>
          </div>
        </main>

        <footer className="footer">
          <p>Impulsado por Google Gemini AI</p>
        </footer>
      </div>
    </div>
  )
}

export default App
