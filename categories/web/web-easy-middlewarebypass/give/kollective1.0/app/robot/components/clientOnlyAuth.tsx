'use client'

import { useRouter } from 'next/navigation'
import { getCookie, deleteCookie } from 'cookies-next'
import Link from 'next/link'

export default function ClientOnlyAuth({ isAuthenticated }: { isAuthenticated: boolean }) {
    const router = useRouter()

    const handleLogout = () => {
        deleteCookie('token')
        router.push('/robot/login')
    }

    return (
        <>
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
                    <button
                        onClick={handleLogout}
                        className="btn btn-outline-danger btn-sm px-3 py-2"
                        style={{
                            fontFamily: "'Orbitron', sans-serif",
                            fontSize: '0.9rem',
                            transition: 'background-color 0.3s',
                        }}
                    >
                        Выйти
                    </button>
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
        </>
    )
}
