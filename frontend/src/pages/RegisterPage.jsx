import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ login: '', password: '', role: 'student' })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)

    if (form.login.length < 6) {
      setError('Логин должен быть не короче 6 символов')
      return
    }
    if (form.password.length < 8) {
      setError('Пароль должен быть не короче 8 символов')
      return
    }

    setLoading(true)
    try {
      await register(form)
      navigate('/', { replace: true })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card card--narrow">
      <h1>Регистрация</h1>
      <form onSubmit={handleSubmit} className="form">
        <label className="field">
          <span>Логин (мин. 6 символов)</span>
          <input value={form.login} onChange={update('login')} autoComplete="username" required />
        </label>
        <label className="field">
          <span>Пароль (мин. 8 символов)</span>
          <input
            type="password"
            value={form.password}
            onChange={update('password')}
            autoComplete="new-password"
            required
          />
        </label>
        <label className="field">
          <span>Роль</span>
          <select value={form.role} onChange={update('role')}>
            <option value="student">Ученик</option>
            <option value="teacher">Учитель</option>
          </select>
        </label>
        {error && <p className="error">{error}</p>}
        <button className="btn btn--primary" disabled={loading}>
          {loading ? 'Создаём…' : 'Зарегистрироваться'}
        </button>
      </form>
      <p className="muted">
        Уже есть аккаунт? <Link to="/login">Войти</Link>
      </p>
    </div>
  )
}
