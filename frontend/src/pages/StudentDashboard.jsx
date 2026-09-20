import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'

export default function StudentDashboard() {
  const [tests, setTests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let active = true
    ;(async () => {
      try {
        const data = await api.listPublishedTests()
        if (active) setTests(data)
      } catch (err) {
        if (active) setError(err.message)
      } finally {
        if (active) setLoading(false)
      }
    })()
    return () => {
      active = false
    }
  }, [])

  return (
    <div>
      <div className="page-head">
        <h1>Доступные тесты</h1>
      </div>

      {error && <p className="error">{error}</p>}
      {loading ? (
        <p className="muted">Загрузка…</p>
      ) : tests.length === 0 ? (
        <div className="empty">
          <p>Пока нет опубликованных тестов.</p>
        </div>
      ) : (
        <ul className="list">
          {tests.map((t) => (
            <li key={t.Id} className="list__item">
              <div className="list__main">
                <span className="list__title">{t.title}</span>
                <div className="list__meta">
                  <span className="muted">{t.questions.length} вопрос(ов)</span>
                </div>
                {t.description && <p className="muted">{t.description}</p>}
              </div>
              <div className="list__actions">
                <Link to={`/student/tests/${t.Id}`} className="btn btn--primary btn--small">
                  Пройти
                </Link>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
