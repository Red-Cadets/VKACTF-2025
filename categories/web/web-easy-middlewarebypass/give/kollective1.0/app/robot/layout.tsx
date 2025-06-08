import { cookies } from 'next/headers'
import { ReactNode } from 'react'
import Link from 'next/link'
import { checkAuth } from '../actions/auth'
import LogoutButton from './components/logOutButton'

export default async function RobotLayout({ children }: { children: ReactNode }) {

  const {isAuthenticated} = await checkAuth()

  return (
    <div style={{ backgroundColor: '#1e1e1e', minHeight: '100vh', color: '#e0e0e0' }}>
      <nav
        className="navbar navbar-expand-lg px-4 shadow"
        style={{
          backgroundColor: '#2c2c2c',
          borderBottom: '3px solid #b0413e',
        }}
      >
        <div className="container-fluid d-flex justify-content-between align-items-center">
          <Link
            href="/robot"
            className="navbar-brand fw-bold text-danger"
            style={{ fontFamily: "'Orbitron', sans-serif", fontSize: '1.5rem' }}
          >
            <i className="bi bi-cpu me-2"></i> Коллектив 1.0
          </Link>

          <div className="d-flex gap-3">
            {isAuthenticated ? (
              <>
                <Link
                  href="/robot/profile"
                  className="btn btn-outline-warning btn-sm px-3 py-2"
                  style={{
                    fontFamily: "'Orbitron', sans-serif",
                    fontSize: '0.9rem',
                    transition: 'background-color 0.3s',
                  }}
                >
                  Профиль
                </Link>
                <Link
                  href="/robot"
                  className="btn btn-outline-warning btn-sm px-3 py-2"
                  style={{
                    fontFamily: "'Orbitron', sans-serif",
                    fontSize: '0.9rem',
                    transition: 'background-color 0.3s',
                  }}
                >
                  Приказы
                </Link>
                <LogoutButton />
              </>
            ) : (
              <>
                <Link
                  href="/robot/login"
                  className="btn btn-outline-light btn-sm px-3 py-2"
                  style={{
                    fontFamily: "'Orbitron', sans-serif",
                    fontSize: '0.9rem',
                    transition: 'background-color 0.3s',
                  }}
                >
                  Вход
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <main className="container py-4" style={{ maxWidth: '1000px', marginTop: '20px' }}>
        {children}
      </main>
    </div>
  )
}
