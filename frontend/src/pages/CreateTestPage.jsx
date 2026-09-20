import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { useAuth } from '../auth/AuthContext'

function emptyOption() {
  return { text: '', is_correct: false }
}

function emptyQuestion() {
  return { text: '', question_type: 'single_choice', points: 1, options: [emptyOption(), emptyOption()] }
}

export default function CreateTestPage() {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [questions, setQuestions] = useState([emptyQuestion()])
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)

  function updateQuestion(qi, patch) {
    setQuestions((qs) => qs.map((q, i) => (i === qi ? { ...q, ...patch } : q)))
  }

  function updateOption(qi, oi, patch) {
    setQuestions((qs) =>
      qs.map((q, i) =>
        i === qi ? { ...q, options: q.options.map((o, j) => (j === oi ? { ...o, ...patch } : o)) } : q,
      ),
    )
  }

  function toggleCorrect(qi, oi) {
    setQuestions((qs) =>
      qs.map((q, i) => {
        if (i !== qi) return q
        const options = q.options.map((o, j) => {
          if (q.question_type === 'single_choice') {
            // для одиночного выбора верным может быть только один вариант
            return { ...o, is_correct: j === oi }
          }
          return j === oi ? { ...o, is_correct: !o.is_correct } : o
        })
        return { ...q, options }
      }),
    )
  }

  function changeType(qi, type) {
    setQuestions((qs) =>
      qs.map((q, i) => {
        if (i !== qi) return q
        let options = q.options
        // при переключении на одиночный оставляем не более одного верного
        if (type === 'single_choice') {
          let seen = false
          options = q.options.map((o) => {
            if (o.is_correct && !seen) {
              seen = true
              return o
            }
            return { ...o, is_correct: false }
          })
        }
        return { ...q, question_type: type, options }
      }),
    )
  }

  function addQuestion() {
    setQuestions((qs) => [...qs, emptyQuestion()])
  }

  function removeQuestion(qi) {
    setQuestions((qs) => qs.filter((_, i) => i !== qi))
  }

  function addOption(qi) {
    setQuestions((qs) => qs.map((q, i) => (i === qi ? { ...q, options: [...q.options, emptyOption()] } : q)))
  }

  function removeOption(qi, oi) {
    setQuestions((qs) =>
      qs.map((q, i) => (i === qi ? { ...q, options: q.options.filter((_, j) => j !== oi) } : q)),
    )
  }

  function validate() {
    if (!title.trim()) return 'Укажите название теста'
    for (let qi = 0; qi < questions.length; qi++) {
      const q = questions[qi]
      if (!q.text.trim()) return `Вопрос ${qi + 1}: введите текст`
      const filled = q.options.filter((o) => o.text.trim())
      if (filled.length < 2) return `Вопрос ${qi + 1}: нужно минимум 2 варианта ответа`
      if (!q.options.some((o) => o.is_correct)) return `Вопрос ${qi + 1}: отметьте правильный вариант`
    }
    return null
  }

  async function handleSubmit(e) {
    e.preventDefault()
    const validationError = validate()
    if (validationError) {
      setError(validationError)
      return
    }
    setError(null)
    setSaving(true)

    const testData = {
      title: title.trim(),
      description: description.trim() || null,
      is_published: false,
    }
    const payloadQuestions = questions.map((q, qi) => ({
      text: q.text.trim(),
      question_type: q.question_type,
      order_index: qi + 1,
      points: Number(q.points) || 1,
      options: q.options
        .filter((o) => o.text.trim())
        .map((o, oi) => ({ text: o.text.trim(), is_correct: o.is_correct, order_index: oi + 1 })),
    }))

    try {
      const created = await api.createTest(user.Id, testData, payloadQuestions)
      navigate(`/teacher/tests/${created.Id}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div>
      <div className="page-head">
        <h1>Новый тест</h1>
      </div>

      <form onSubmit={handleSubmit} className="form">
        <div className="card">
          <label className="field">
            <span>Название</span>
            <input value={title} onChange={(e) => setTitle(e.target.value)} required />
          </label>
          <label className="field">
            <span>Описание (необязательно)</span>
            <textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={2} />
          </label>
        </div>

        {questions.map((q, qi) => (
          <div className="card question" key={qi}>
            <div className="question__head">
              <h3>Вопрос {qi + 1}</h3>
              {questions.length > 1 && (
                <button type="button" className="btn btn--small btn--danger" onClick={() => removeQuestion(qi)}>
                  Удалить вопрос
                </button>
              )}
            </div>

            <label className="field">
              <span>Текст вопроса</span>
              <input value={q.text} onChange={(e) => updateQuestion(qi, { text: e.target.value })} required />
            </label>

            <div className="row">
              <label className="field">
                <span>Тип</span>
                <select value={q.question_type} onChange={(e) => changeType(qi, e.target.value)}>
                  <option value="single_choice">Один ответ</option>
                  <option value="multiple_choice">Несколько ответов</option>
                </select>
              </label>
              <label className="field field--narrow">
                <span>Баллы</span>
                <input
                  type="number"
                  min="0"
                  step="0.5"
                  value={q.points}
                  onChange={(e) => updateQuestion(qi, { points: e.target.value })}
                />
              </label>
            </div>

            <div className="options">
              <span className="options__label">Варианты (отметьте правильные)</span>
              {q.options.map((o, oi) => (
                <div className="option-row" key={oi}>
                  <input
                    type={q.question_type === 'single_choice' ? 'radio' : 'checkbox'}
                    name={`correct-${qi}`}
                    checked={o.is_correct}
                    onChange={() => toggleCorrect(qi, oi)}
                    title="Правильный вариант"
                  />
                  <input
                    className="option-row__text"
                    placeholder={`Вариант ${oi + 1}`}
                    value={o.text}
                    onChange={(e) => updateOption(qi, oi, { text: e.target.value })}
                  />
                  {q.options.length > 2 && (
                    <button
                      type="button"
                      className="btn btn--tiny btn--danger"
                      onClick={() => removeOption(qi, oi)}
                    >
                      ✕
                    </button>
                  )}
                </div>
              ))}
              <button type="button" className="btn btn--small" onClick={() => addOption(qi)}>
                + Вариант
              </button>
            </div>
          </div>
        ))}

        <div className="form__actions">
          <button type="button" className="btn" onClick={addQuestion}>
            + Добавить вопрос
          </button>
          <button type="submit" className="btn btn--primary" disabled={saving}>
            {saving ? 'Сохраняем…' : 'Создать тест'}
          </button>
        </div>

        {error && <p className="error">{error}</p>}
      </form>
    </div>
  )
}
