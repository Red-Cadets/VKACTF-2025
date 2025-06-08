'use client'

import "bootstrap/dist/css/bootstrap.min.css"
import "../globals.css"
import { ReactNode } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"


export default function Layout({ children }: { children: ReactNode }) {
  const pathname = usePathname()

  return (
    <div
      className="d-flex"
      style={{ minHeight: '100vh', backgroundColor: '#2c2c2c', color: '#e0e0e0' }}
    >
      <aside
        className="d-flex flex-column p-3 text-white"
        style={{
          width: '240px',
          backgroundColor: '#1e1e1e',
          borderRight: '2px solid #444',
          boxShadow: '4px 0 6px rgba(0,0,0,0.5)'
        }}
      >
        <h2
          className="text-uppercase fw-bold mb-4"
          style={{
            fontFamily: "'Orbitron', sans-serif",
            fontSize: '1.3rem',
            color: '#d1a75f'
          }}
        >
          <i className="bi bi-cpu me-2"></i>
          Комплекс 3826
        </h2>
        <ul className="nav nav-pills flex-column mb-auto gap-2">
          <li className="nav-item">
            <Link
              href="/admin"
              className={`nav-link rounded fw-semibold ${pathname === '/admin' ? 'bg-danger text-white' : 'text-light'
                }`}
            >
              <i className="bi bi-robot me-2"></i> Роботы
            </Link>
          </li>
          <li>
            <Link
              href="/admin/model"
              className={`nav-link rounded fw-semibold ${pathname === '/admin/model' ? 'bg-danger text-white' : 'text-light'
                }`}
            >
              <i className="bi bi-gear-wide-connected me-2"></i> Модели
            </Link>
          </li>
          <li>
            <Link
              href="/admin/orders"
              className={`nav-link rounded fw-semibold ${pathname === '/admin/orders' ? 'bg-danger text-white' : 'text-light'
                }`}
            >
              <i className="bi bi-file-earmark-text me-2"></i> Приказы
            </Link>
          </li>
          <li>
            <Link
              href="/admin/dump"
              className={`nav-link rounded fw-semibold ${pathname === '/admin/dump' ? 'bg-danger text-white' : 'text-light'
                }`}
            >
              <i className="bi bi-cloud-upload me-2"></i> Загрузить дамп
            </Link>
          </li>
        </ul>
        <hr style={{ borderColor: '#444' }} />
        <div className="small text-light">v2.1.0 • СССР</div>
      </aside>

      <main className="flex-grow-1 p-4">
        <header className="mb-5 d-flex align-items-center">
          <i
            className="bi bi-gear-fill me-3"
            style={{ fontSize: '2.5rem', color: '#b0413e' }}
          ></i>
          <div>
            <h1
              className="fw-bold mb-1"
              style={{ fontFamily: "'Orbitron', sans-serif", color: '#b0413e' }}
            >
              Коллектив 1.0
            </h1>
            <p className="text mb-0">Панель администрирования</p>
          </div>
        </header>

        {children}
      </main>
    </div>
  )
}
