// Тонкая обёртка над fetch для общения с бэкендом.
// Все пути начинаются с /api и в dev-режиме проксируются Vite на бэкенд.

const BASE = import.meta.env.VITE_API_BASE ?? ''

function extractError(data, status) {
  if (data && typeof data === 'object') {
    const detail = data.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) {
      // Ошибки валидации Pydantic: [{loc, msg, ...}]
      return detail.map((d) => d.msg || JSON.stringify(d)).join('; ')
    }
  }
  return `Ошибка запроса (${status})`
}

async function request(path, { method = 'GET', body } = {}) {
  const options = { method, headers: {} }
  if (body !== undefined) {
    options.headers['Content-Type'] = 'application/json'
    options.body = JSON.stringify(body)
  }

  const resp = await fetch(`${BASE}${path}`, options)

  if (resp.status === 204) return null

  let data = null
  const text = await resp.text()
  if (text) {
    try {
      data = JSON.parse(text)
    } catch {
      data = text
    }
  }

  if (!resp.ok) {
    throw new Error(extractError(data, resp.status))
  }
  return data
}

export const api = {
  // --- Пользователи ---
  register: (payload) => request('/api/users/register', { method: 'POST', body: payload }),
  login: (payload) => request('/api/users/login', { method: 'POST', body: payload }),
  getUser: (id) => request(`/api/users/${id}`),

  // --- Тесты ---
  listPublishedTests: () => request('/api/test/'),
  listAuthorTests: (authorId) => request(`/api/test/by-author/${authorId}`),
  getTest: (id) => request(`/api/test/${id}`),
  takeTest: (id) => request(`/api/test/${id}/take`),
  createTest: (authorId, testData, questions) =>
    request(`/api/test/create?author_id=${authorId}`, {
      method: 'POST',
      body: { test_data: testData, questions },
    }),
  updateTest: (id, payload) => request(`/api/test/${id}`, { method: 'PATCH', body: payload }),
  publishTest: (id) => request(`/api/test/${id}/publish`, { method: 'POST' }),
  deleteTest: (id) => request(`/api/test/${id}`, { method: 'DELETE' }),

  // --- Попытки прохождения ---
  startAttempt: (userId, testId) =>
    request(`/api/attempt/start?user_id=${userId}`, { method: 'POST', body: { test_id: testId } }),
  submitAnswer: (attemptId, payload) =>
    request(`/api/attempt/${attemptId}/answer`, { method: 'POST', body: payload }),
  finishAttempt: (attemptId) => request(`/api/attempt/${attemptId}/finish`, { method: 'POST' }),
  getAttempt: (attemptId) => request(`/api/attempt/${attemptId}`),

  // --- Группы ---
  createGroup: (payload) => request('/api/group/', { method: 'POST', body: payload }),
  addStudent: (groupId, userId) =>
    request(`/api/group/${groupId}/students/${userId}`, { method: 'POST' }),
  listStudents: (groupId) => request(`/api/group/${groupId}/students`),
}
