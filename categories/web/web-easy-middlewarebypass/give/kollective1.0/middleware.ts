import { NextRequest, NextResponse } from 'next/server'
import { getToken } from './app/actions/auth'



export default async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl
  if (pathname.startsWith('/login-admin-panel')) {
    const res = NextResponse.next()
    res.cookies.delete('token')
    return res
  }
  if (pathname.startsWith('/admin')) {
    const token = req.cookies.get('token')?.value

    if (!token) {
      return NextResponse.redirect(new URL('/login-admin-panel', req.url))
    }

    const payload = await getToken(token)

    if (!payload || !payload.admin) {
      return NextResponse.redirect(new URL('/login-admin-panel', req.url))
    }

    return NextResponse.next()
  }

  return NextResponse.next()
}
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|.*\\.png$).*)'],
}
