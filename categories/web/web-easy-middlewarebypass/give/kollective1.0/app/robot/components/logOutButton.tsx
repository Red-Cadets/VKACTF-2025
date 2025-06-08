'use client'

import { useRouter } from 'next/navigation'
import { useTransition } from 'react'
import { logout } from '../../actions/logout'

export default function LogoutButton() {
    const router = useRouter()
    const [isPending, startTransition] = useTransition()

    const handleLogout = async () => {
        startTransition(async () => {
            await logout()
        })
    }

    return (
        <button
            onClick={handleLogout}
            className="btn btn-outline-danger btn-sm px-3 py-2"
            style={{
                fontFamily: "'Orbitron', sans-serif",
                fontSize: '0.9rem',
                transition: 'background-color 0.3s',
            }}
        >
            {isPending ? 'Выход...' : 'Выйти'}
        </button>
    )
}
