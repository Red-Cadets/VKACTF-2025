'use client'

import { useState, useEffect } from 'react'
import { getCookie, deleteCookie } from 'cookies-next'
import { useRouter } from 'next/navigation'
import { getRobot } from '@/app/actions/getRobot'
import { updateBio } from '@/app/actions/updateBio'
import { getAllModels } from '@/app/actions/getModels'

export default function RobotProfilePage() {
  const [profile, setProfile] = useState<any>(null)
  const [modelId, setModelId] = useState<any>(null)
  const [models, setModels] = useState<{ id: number; name: string; combat: boolean }[]>([])
  const [bio, setBio] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const router = useRouter()

  useEffect(() => {
    getAllModels()
      .then(setModels)
      .catch(() => setError('Ошибка загрузки моделей'))

    document.body.style.background = `radial-gradient(circle at center, #0c0c0c, #1a1a1a)`
    document.body.style.minHeight = '100vh'
    document.body.style.fontFamily = "'Orbitron', sans-serif"
    document.body.style.margin = '0'

    return () => {
      document.body.style.background = ''
      document.body.style.minHeight = ''
      document.body.style.fontFamily = ''
      document.body.style.margin = ''
    }
  }, [])

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const profile = await getRobot()
        if ('error' in profile) {
          setError('Ошибка при загрузке профиля')
        } else {
          setProfile(profile)
          setBio(profile.bio || '')
          setModelId(profile.modelId || null)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Произошла ошибка')
      } finally {
        setIsLoading(false)
      }
    }

    fetchProfile()
  }, [])

  const handleUpdateBio = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    try {
      const profile = await updateBio(bio, modelId)

      if ('error' in profile) {
        setError(profile.error)
      } else {
        setProfile(profile)
        setBio(profile.bio || '')
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла ошибка')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDeleteAccount = async () => {
    if (confirm('Вы уверены, что хотите удалить свою учетную запись?')) {
      setIsLoading(true)
      try {
        deleteCookie('token')
        router.push('/robot/login')
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Произошла ошибка')
      } finally {
        setIsLoading(false)
      }
    }
  }

  if (isLoading) {
    return <div className="text-light text-center mt-5">Загрузка...</div>
  }

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4 text-danger fw-bold text-shadow">Профиль робота</h1>

      {error && <div className="alert alert-danger text-center">{error}</div>}

      <div className="card shadow-lg p-4 bg-dark border-0 text-light rounded-4 mx-auto" style={{ maxWidth: '500px' }}>
        <div className="text-center mb-4">
          <img
            src="https://robohash.org/robot.png?size=150x150"
            alt="Аватар робота"
            className="rounded-circle border border-danger"
            width="150"
            height="150"
          />
        </div>

        <form onSubmit={handleUpdateBio}>
          <div className="mb-3">
            <label htmlFor="bio" className="form-label text-danger">Биография</label>
            <textarea
              id="bio"
              className="form-control bg-dark text-light border-danger shadow-sm"
              rows={4}
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              placeholder="Введите информацию о себе..."
            />
          </div>
          <div className="mb-3">
            <label className="form-label text-danger">Модель</label>
            <select
              className="form-select bg-black text-light border-danger shadow-sm"
              name="modelId"
              value={modelId ?? ''}
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

          <button type="submit" className="btn btn-danger w-100 fw-bold mt-3" disabled={isLoading}>
            {isLoading ? (
              <>
                <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true" />
                Обновление...
              </>
            ) : (
              'Обновить'
            )}
          </button>
        </form>
      </div>

      {profile && (
        <div className="mt-5 text-center text-light">
          <h4 className="text-danger fw-bold mb-3 text-shadow">Информация о роботе</h4>
          <div className="d-flex flex-column align-items-center">
            <p><strong>Имя:</strong> {profile.name}</p>
            <p><strong>Модель:</strong> {profile.model?.name || 'Неизвестно'}</p>
          </div>
        </div>
      )}

      <div className="text-center mt-5">
        <button
          onClick={handleDeleteAccount}
          className="btn btn-outline-danger w-100 fw-bold mt-3"
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true" />
              Удаление...
            </>
          ) : (
            'Удалить учетную запись'
          )}
        </button>
      </div>
    </div>
  )
}
