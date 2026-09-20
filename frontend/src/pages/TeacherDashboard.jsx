import { useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api/client'
import { useAuth } from '../auth/AuthContext'

export default function TeacherDashboard() {
  const { user } = useAuth()
  const [tests, setTests] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [busyId, setBusyId] = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.listAuthorTests(user.Id)
      setTests(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [user.Id])

  useEffect(() => {
    load()
  }, [load])

  async function handlePublish(id) {
    setBusyId(id)
    try {
      await api.publishTest(id)
      await load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusyId(null)
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Удалить тест? Действие необратимо.')) return
    setBusyId(id)
    try {
      await api.deleteTest(id)
      setTests((list) => list.filter((t) => t.Id !== id))
    } catch (err) {
      setError(err.message)
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div>
      <div className="page-head">
        <h1>Мои тесты</h1>
        <Link to="/teacher/new" className="btn btn--primary">
          + Создать тест
        </Link>
      </div>

      {error && <p className="error">{error}</p>}
      {loading ? (
        <p className="muted">Загрузка…</p>
      ) : tests.length === 0 ? (
        <div className="empty">
          <p>Пока нет ни одного теста.</p>
          <Link to="/teacher/new" className="btn btn--primary">
            Создать первый тест
          </Link>
        </div>
      ) : (
        <ul className="list">
          {tests.map((t) => (
            <li key={t.Id} className="list__item">
              <div className="list__main">
                <Link to={`/teacher/tests/${t.Id}`} className="list__title">
                  {t.title}
                </Link>
                <div className="list__meta">
                  <span className={`tag ${t.is_published ? 'tag--green' : 'tag--gray'}`}>
                    {t.is_published ? 'Опубликован' : 'Черновик'}
                  </span>
                  <span className="muted">{t.questions.length} вопрос(ов)</span>
                </div>
                {t.description && <p className="muted">{t.description}</p>}
              </div>
              <div className="list__actions">
                {!t.is_published && (
                  <button
                    className="btn btn--small"
                    disabled={busyId === t.Id}
                    onClick={() => handlePublish(t.Id)}
                  >
                    Опубликовать
                  </button>
                )}
                <button
                  className="btn btn--small btn--danger"
                  disabled={busyId === t.Id}
                  onClick={() => handleDelete(t.Id)}
                >
                  Удалить
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
