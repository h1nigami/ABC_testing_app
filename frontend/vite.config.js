import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Бэкенд по умолчанию слушает http://127.0.0.1:8000.
// В dev-режиме запросы к /api проксируются на него, чтобы избежать CORS.
const BACKEND_URL = process.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: BACKEND_URL,
        changeOrigin: true,
      },
    },
  },
})
