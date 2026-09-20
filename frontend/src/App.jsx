import { Navigate, Route, Routes } from 'react-router-dom'
import Nav from './components/Nav'
import ProtectedRoute from './components/ProtectedRoute'
import { useAuth } from './auth/AuthContext'

import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import TeacherDashboard from './pages/TeacherDashboard'
import CreateTestPage from './pages/CreateTestPage'
import TestDetailPage from './pages/TestDetailPage'
import StudentDashboard from './pages/StudentDashboard'
import TakeTestPage from './pages/TakeTestPage'

function Home() {
  const { isAuthenticated, isTeacher } = useAuth()
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return <Navigate to={isTeacher ? '/teacher' : '/student'} replace />
}

export default function App() {
  return (
    <>
      <Nav />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route
            path="/teacher"
            element={
              <ProtectedRoute role="teacher">
                <TeacherDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/teacher/new"
            element={
              <ProtectedRoute role="teacher">
                <CreateTestPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/teacher/tests/:testId"
            element={
              <ProtectedRoute role="teacher">
                <TestDetailPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/student"
            element={
              <ProtectedRoute role="student">
                <StudentDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/tests/:testId"
            element={
              <ProtectedRoute role="student">
                <TakeTestPage />
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </>
  )
}
