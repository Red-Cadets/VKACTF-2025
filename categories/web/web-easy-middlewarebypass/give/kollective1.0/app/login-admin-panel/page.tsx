'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { deleteCookie, setCookie } from 'cookies-next'
import { adminLogin } from '../actions/adminLogin'

export default function AdminLoginPage() {
  const [login, setLogin] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const router = useRouter()

  useEffect(() => {
    document.body.style.background = `linear-gradient(145deg, #1b1f22, #292e33)`
    document.body.style.backgroundSize = 'cover'
    document.body.style.minHeight = '100vh'
    document.body.style.margin = '0'
    document.body.style.fontFamily = "'Orbitron', sans-serif"

    return () => {
      document.body.style.background = ''
      document.body.style.backgroundSize = ''
      document.body.style.minHeight = ''
      document.body.style.margin = ''
      document.body.style.fontFamily = ''
    }
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      deleteCookie('token')
      const response = await adminLogin({ login, password })
      if (response.error) {
        throw new Error(response.error || 'Ошибка авторизации')
      }

      if (response.token) {

        setCookie('token', response.token)
        router.push('/admin')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла неизвестная ошибка')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="d-flex align-items-center justify-content-center min-vh-100">
      <div className="card bg-dark border-danger text-light p-5 shadow-lg rounded-4" style={{ maxWidth: '420px', width: '100%' }}>
        <h1 className="text-center mb-4 text-danger fw-bold">ПАНЕЛЬ АДМИНИСТРАТОРА</h1>

        {error && (
          <div className="alert alert-danger text-center">{error}</div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="login" className="text-light form-label">Логин</label>
            <input
              id="login"
              type="text"
              className="form-control bg-black text-light border-danger"
              placeholder="admin"
              value={login}
              onChange={(e) => setLogin(e.target.value)}
              required
            />
          </div>

          <div className="mb-4">
            <label htmlFor="password" className="text-light form-label">Пароль</label>
            <input
              id="password"
              type="password"
              className="form-control bg-black text-light border-danger"
              placeholder="••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" disabled={isLoading} className="btn btn-danger w-100 fw-bold">
            {isLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true" />
                Вход...
              </>
            ) : (
              'Войти'
            )}
          </button>
        </form>
      </div>
    </div>
  )
}
