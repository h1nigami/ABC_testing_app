import { useCallback, useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api/client'
import { useAuth } from '../auth/AuthContext'

export default function TakeTestPage() {
  const { testId } = useParams()
  const { user } = useAuth()

  const [test, setTest] = useState(null)
  const [attempt, setAttempt] = useState(null)
  const [answers, setAnswers] = useState({}) // questionId -> [optionId]
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const start = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const testData = await api.takeTest(testId)
      setTest(testData)
      const attemptData = await api.startAttempt(user.Id, Number(testId))
      setAttempt(attemptData)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [testId, user.Id])

  useEffect(() => {
    start()
  }, [start])

  function selectSingle(questionId, optionId) {
    setAnswers((a) => ({ ...a, [questionId]: [optionId] }))
  }

  function toggleMultiple(questionId, optionId) {
    setAnswers((a) => {
      const current = a[questionId] || []
      const next = current.includes(optionId)
        ? current.filter((id) => id !== optionId)
        : [...current, optionId]
      return { ...a, [questionId]: next }
    })
  }

  async function handleSubmit() {
    if (!attempt) return
    setSubmitting(true)
    setError(null)
    try {
      for (const q of test.questions) {
        const selected = answers[q.Id] || []
        for (const optionId of selected) {
          await api.submitAnswer(attempt.Id, {
            attempt_id: attempt.Id,
            question_id: q.Id,
            selected_option_id: optionId,
          })
        }
      }
      const finished = await api.finishAttempt(attempt.Id)
      setResult(finished)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <p className="muted">Загрузка…</p>
  if (error && !test) return <p className="error">{error}</p>
  if (!test) return null

  const maxScore = test.questions.reduce((sum, q) => sum + (q.points || 0), 0)
  const sortedQuestions = [...test.questions].sort((a, b) => a.order_index - b.order_index)

  if (result) {
    return (
      <div className="card card--narrow result">
        <h1>Тест завершён</h1>
        <p className="result__score">
          {result.score} <span className="muted">/ {maxScore}</span>
        </p>
        <p className="muted">баллов набрано</p>
        <Link to="/student" className="btn btn--primary">
          К списку тестов
        </Link>
      </div>
    )
  }

  return (
    <div>
      <div className="page-head">
        <div>
          <Link to="/student" className="muted">
            ← К списку тестов
          </Link>
          <h1>{test.title}</h1>
        </div>
        <span className="muted">Максимум: {maxScore} балл(ов)</span>
      </div>
      {test.description && <p className="muted">{test.description}</p>}

      {sortedQuestions.map((q, qi) => {
        const options = [...q.options].sort((a, b) => a.order_index - b.order_index)
        const selected = answers[q.Id] || []
        const multiple = q.question_type === 'multiple_choice'
        return (
          <div className="card" key={q.Id}>
            <div className="question__head">
              <h3>
                {qi + 1}. {q.text}
              </h3>
              <span className="muted">{multiple ? 'Несколько ответов' : 'Один ответ'}</span>
            </div>
            <ul className="answers">
              {options.map((o) => (
                <li key={o.Id} className="answers__item">
                  <label className="answers__choice">
                    <input
                      type={multiple ? 'checkbox' : 'radio'}
                      name={`q-${q.Id}`}
                      checked={selected.includes(o.Id)}
                      onChange={() => (multiple ? toggleMultiple(q.Id, o.Id) : selectSingle(q.Id, o.Id))}
                    />
                    <span>{o.text}</span>
                  </label>
                </li>
              ))}
            </ul>
          </div>
        )
      })}

      {error && <p className="error">{error}</p>}
      <div className="form__actions">
        <button className="btn btn--primary" onClick={handleSubmit} disabled={submitting}>
          {submitting ? 'Отправляем…' : 'Завершить тест'}
        </button>
      </div>
    </div>
  )
}
