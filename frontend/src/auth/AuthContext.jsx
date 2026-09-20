import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { api } from '../api/client'

const STORAGE_KEY = 'abc_user'
const AuthContext = createContext(null)

function loadStoredUser() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(loadStoredUser)

  useEffect(() => {
    try {
      if (user) localStorage.setItem(STORAGE_KEY, JSON.stringify(user))
      else localStorage.removeItem(STORAGE_KEY)
    } catch {
      /* localStorage может быть недоступен — работаем в памяти */
    }
  }, [user])

  const value = useMemo(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isTeacher: user?.role === 'teacher',
      async login(credentials) {
        const u = await api.login(credentials)
        setUser(u)
        return u
      },
      async register(payload) {
        const u = await api.register(payload)
        setUser(u)
        return u
      },
      logout() {
        setUser(null)
      },
    }),
    [user],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth должен использоваться внутри AuthProvider')
  return ctx
}
