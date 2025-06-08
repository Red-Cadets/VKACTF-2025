'use client'

import { useEffect, useState } from 'react'
import { getAllRobots } from '../actions/getRobots'

interface Robot {
  id: number
  name: string
  bio: string | null
  modelId: number
  model: {
    name: string
  }
}

export default function RobotsPage() {
  const [robots, setRobots] = useState<Robot[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')


  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const result = await getAllRobots()

        if ('error' in result) {
          setError(result.error)
        } else {
          setRobots(result)

        }
        setLoading(false)
      } catch (err) {
        setError('Ошибка загрузки приказов')
      }
    }

    fetchOrders()
  }, [])


  return (
    <div className="container py-5">
      <h1 className="display-4 text-center fw-bold mb-5 text-light border-bottom border-danger pb-3">
        РОБОТЫ КОМПЛЕКСА
      </h1>

      {error && (
        <div className="alert alert-danger shadow-sm" role="alert">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center text-secondary py-5">
          <div className="spinner-border text-danger mb-3" role="status" />
          <p>Загрузка роботов...</p>
        </div>
      ) : (
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          {robots.map((robot) => (
            <div key={robot.id} className="col">
              <div className="card h-100 bg-dark text-light border border-danger shadow-lg rounded-4">
                <div className="card-body">
                  <h5 className="card-title text-accent fw-bold fs-4 mb-1">
                    🤖 {robot.name}
                  </h5>
                  <span className="badge bg-danger text-light mb-3">
                    Модель: {robot.model.name}
                  </span>
                  <p className="card-text text-secondary">
                    {robot.bio || 'Описание отсутствует'}
                  </p>
                </div>
                <div className="card-footer border-top border-secondary text-end bg-transparent">
                  <small className="text-muted">ID: {robot.id}</small>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
