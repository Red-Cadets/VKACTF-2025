'use client'

import Link from 'next/link'

export default function HomePage() {
  return (
    <div style={{
      position: 'relative',
      background: 'url("https://wylsa.com/wp-content/uploads/2023/02/atomicheart16.jpg") center/cover no-repeat',
      minHeight: '100vh',
      fontFamily: "'Orbitron', sans-serif'",
      color: '#fff'
    }}>
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        zIndex: 1
      }}></div>

      <div className="container text-center py-5" style={{ zIndex: 2, position: 'relative' }}>
        <div className="row justify-content-center">
          <div className="col-lg-8 col-md-10">
            <h1 className="display-4 text-danger fw-bold mb-4">
              Добро пожаловать в Коллектив 1.0!
            </h1>
            <p className="lead mb-4 text-light">
              Здесь вы можете зарегистрировать своего робота, управлять его настройками и получить доступ к секретным данным.
              Войдите в систему или создайте нового робота, чтобы начать.
            </p>



            <Link
              href="/robot"
              className="btn btn-lg btn-danger fw-bold py-3 px-5 rounded-4 shadow-lg"
              style={{ fontSize: '1.2rem' }}
            >
              Перейти в раздел роботов
            </Link>
          </div>
        </div>
      </div>

      <footer
        className="text-center text-light py-3"
        style={{ backgroundColor: '#1a1a1a', position: 'absolute', bottom: 0, width: '100%' }}
      >
        <p>&copy; 2025 Коллектив 1.0. Все права защищены.</p>
      </footer>
    </div>
  )
}
