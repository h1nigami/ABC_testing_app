import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { api } from '../api/client'

const TYPE_LABEL = {
  single_choice: 'Один ответ',
  multiple_choice: 'Несколько ответов',
}

export default function TestDetailPage() {
  const { testId } = useParams()
  const navigate = useNavigate()
  const [test, setTest] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      setTest(await api.getTest(testId))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [testId])

  useEffect(() => {
    load()
  }, [load])

  async function handlePublish() {
    setBusy(true)
    try {
      await api.publishTest(testId)
      await load()
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  async function handleDelete() {
    if (!window.confirm('Удалить тест? Действие необратимо.')) return
    setBusy(true)
    try {
      await api.deleteTest(testId)
      navigate('/teacher')
    } catch (err) {
      setError(err.message)
      setBusy(false)
    }
  }

  if (loading) return <p className="muted">Загрузка…</p>
  if (error) return <p className="error">{error}</p>
  if (!test) return null

  const sortedQuestions = [...test.questions].sort((a, b) => a.order_index - b.order_index)

  return (
    <div>
      <div className="page-head">
        <div>
          <Link to="/teacher" className="muted">
            ← К списку тестов
          </Link>
          <h1>{test.title}</h1>
          <span className={`tag ${test.is_published ? 'tag--green' : 'tag--gray'}`}>
            {test.is_published ? 'Опубликован' : 'Черновик'}
          </span>
        </div>
        <div className="list__actions">
          {!test.is_published && (
            <button className="btn btn--primary" onClick={handlePublish} disabled={busy}>
              Опубликовать
            </button>
          )}
          <button className="btn btn--danger" onClick={handleDelete} disabled={busy}>
            Удалить
          </button>
        </div>
      </div>

      {test.description && <p className="muted">{test.description}</p>}

      {sortedQuestions.length === 0 ? (
        <p className="muted">В тесте пока нет вопросов.</p>
      ) : (
        sortedQuestions.map((q, qi) => {
          const options = [...q.options].sort((a, b) => a.order_index - b.order_index)
          return (
            <div className="card" key={q.Id}>
              <div className="question__head">
                <h3>
                  {qi + 1}. {q.text}
                </h3>
                <span className="muted">
                  {TYPE_LABEL[q.question_type] || q.question_type} · {q.points} балл(ов)
                </span>
              </div>
              <ul className="answers">
                {options.map((o) => (
                  <li key={o.Id} className={o.is_correct ? 'answers__item answers__item--correct' : 'answers__item'}>
                    {o.is_correct ? '✔ ' : '• '}
                    {o.text}
                  </li>
                ))}
              </ul>
            </div>
          )
        })
      )}
    </div>
  )
}
