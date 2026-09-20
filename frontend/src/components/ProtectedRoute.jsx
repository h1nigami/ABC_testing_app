import { Navigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

// Пускает только авторизованных; при указании role — только нужную роль.
export default function ProtectedRoute({ children, role }) {
  const { isAuthenticated, user } = useAuth()

  if (!isAuthenticated) return <Navigate to="/login" replace />
  if (role && user.role !== role) return <Navigate to="/" replace />
  return children
}
