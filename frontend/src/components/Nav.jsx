import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export default function Nav() {
  const { user, isAuthenticated, isTeacher, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <header className="nav">
      <div className="nav__inner">
        <Link to="/" className="nav__brand">
          ABC&nbsp;Testing
        </Link>
        <nav className="nav__links">
          {isAuthenticated && isTeacher && (
            <>
              <Link to="/teacher">Мои тесты</Link>
              <Link to="/teacher/new">Создать тест</Link>
            </>
          )}
          {isAuthenticated && !isTeacher && <Link to="/student">Тесты</Link>}
        </nav>
        <div className="nav__user">
          {isAuthenticated ? (
            <>
              <span className="nav__badge">
                {user.login} · {user.role === 'teacher' ? 'учитель' : 'ученик'}
              </span>
              <button className="btn btn--ghost" onClick={handleLogout}>
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link to="/login">Вход</Link>
              <Link to="/register">Регистрация</Link>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
