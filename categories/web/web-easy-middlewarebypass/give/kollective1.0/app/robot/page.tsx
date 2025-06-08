'use client'

import { useEffect, useState } from 'react'
import { getOrders } from '../actions/getOrders'

interface Order {
  id: number
  message: string
  model: {
    name: string
  }
}

export default function RobotOrdersPage() {
  const [orders, setOrders] = useState<Order[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const result = await getOrders()

        if ('error' in result) {
          setError(result.error)
        } else {
          setOrders(result)
        }
      } catch (err) {
        setError('Ошибка загрузки приказов')
      }
    }

    fetchOrders()
  }, [])

  return (
    <div className="d-flex align-items-center justify-content-center min-vh-100">
      <div className="card bg-dark border-danger text-light p-5 shadow-lg rounded-4 w-100" style={{ maxWidth: '900px' }}>
        <h1 className="text-center mb-5 text-danger fw-bold" style={{ fontFamily: "'Orbitron', sans-serif" }}>
          АКТИВНЫЕ ПРИКАЗЫ
        </h1>

        {error && (
          <div className="alert alert-danger shadow-sm text-center" role="alert">
            {error} <br></br>
            <a href="/robot/login" className="text-decoration-underline text-alert">Войдите</a> в учётную запись.
          </div>
        )}

        {!error && (
          <div className="row row-cols-1 row-cols-md-2 g-4">
            {orders.map((order) => (
              <div key={order.id} className="col">
                <div className="card h-100 bg-black text-light border border-danger shadow-sm">
                  <div className="card-body">
                    <h5 className="card-title text-danger" style={{ fontFamily: "'Orbitron', sans-serif" }}>
                      Модель: {order.model.name}
                    </h5>
                    <p className="card-text">{order.message}</p>
                  </div>
                  <div className="card-footer border-top border-danger text-end">
                    <small className="text-muted">ID: {order.id}</small>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
