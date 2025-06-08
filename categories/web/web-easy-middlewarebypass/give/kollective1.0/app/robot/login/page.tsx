'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { loginRobot, registerRobot } from '../../actions/createRobot'
import { getAllModels } from '@/app/actions/getModels'

export default function RobotAuthPage() {
  const [tab, setTab] = useState<'login' | 'register'>('login')
  const [login, setLogin] = useState('')
  const [password, setPassword] = useState('')
  const [repeatPassword, setRepeatPassword] = useState('')
  const [modelId, setModelId] = useState<number | null>(null)
  const [models, setModels] = useState<{ id: number; name: string; combat: boolean }[]>([])
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

  useEffect(() => {
    getAllModels()
      .then(setModels)
      .catch(() => setError('Ошибка загрузки моделей'))
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    try {
      if (tab === 'login') {
        const result = await loginRobot({
          name: login,
          password: password,
        })
        if (result.error) {
          setError(result.error)
        } else {
          router.push('/robot/profile')
        }
      } else if (tab === 'register') {
        const result = await registerRobot({
          name: login,
          password: password,
          repass: repeatPassword,
          modelId: modelId || 1,
        })
        if (result.error) {
          setError(result.error)
        } else {
          router.push('/robot/profile')
        }
      }
    } catch (err) {
      setError('Произошла ошибка при обработке запроса')
    } finally {
      setIsLoading(false)
    }
  }


  return (
    <div className="d-flex align-items-center justify-content-center min-vh-100">
      <div className="card bg-dark border-danger text-light p-5 shadow-lg rounded-4" style={{ maxWidth: '460px', width: '100%' }}>
        <div className="d-flex justify-content-center mb-4 gap-2">
          <button
            onClick={() => setTab('login')}
            className={`btn fw-bold ${tab === 'login' ? 'btn-danger' : 'btn-outline-danger'}`}
          >
            Вход
          </button>
          <button
            onClick={() => setTab('register')}
            className={`btn fw-bold ${tab === 'register' ? 'btn-danger' : 'btn-outline-danger'}`}
          >
            Регистрация
          </button>
        </div>

        <h2 className="text-center mb-4 text-danger fw-bold">
          {tab === 'login' ? 'Вход в систему' : 'Регистрация робота'}
        </h2>

        {error && <div className="alert alert-danger text-center">{error}</div>}

        <form onSubmit={handleSubmit} method="POST">
          <div className="mb-3">
            <label className="form-label text-light">Логин</label>
            <input
              type="text"
              name="login"
              className="form-control bg-black text-light border-danger"
              value={login}
              onChange={e => setLogin(e.target.value)}
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label text-light">Пароль</label>
            <input
              type="password"
              name="password"
              className="form-control bg-black text-light border-danger"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
            />
          </div>

          {tab === 'register' && (
            <>
              <div className="mb-3">
                <label className=" text-light form-label">Повтор пароля</label>
                <input
                  type="password"
                  name="repeatPassword"
                  className="form-control bg-black text-light border-danger"
                  value={repeatPassword}
                  onChange={e => setRepeatPassword(e.target.value)}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Модель</label>
                <select
                  className="form-select bg-black text-light border-danger"
                  name="modelId"
                  value={modelId || ''}
                  onChange={e => setModelId(Number(e.target.value))}
                  required
                >
                  <option value="" disabled>
                    Выберите модель
                  </option>
                  {models.map(model => (
                    <option key={model.id} value={model.id} style={{ color: model?.combat ? '#b0413e' : 'inherit' }}>
                      {model.name}
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}

          <button type="submit" disabled={isLoading} className="btn btn-danger w-100 fw-bold">
            {isLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true" />
                {tab === 'login' ? 'Вход...' : 'Регистрация...'}
              </>
            ) : (
              tab === 'login' ? 'Войти' : 'Зарегистрироваться'
            )}
          </button>
        </form>
      </div>
    </div>
  )
}
