import { JWTPayload, jwtVerify, SignJWT } from 'jose'
import { cookies } from 'next/headers'

const JWT_SECRET = process.env.JWT_SECRET || 'your_secret_key'

export async function signToken(payload: JWTPayload) {
  const secret = new TextEncoder().encode(JWT_SECRET!)
  const token = await new SignJWT(payload)
  .setProtectedHeader({ alg: 'HS256' })
  .setExpirationTime('1h')
  .sign(secret)
  return token
}
export async function getToken(token:string){
  try{
    return (await jwtVerify(token, new TextEncoder().encode(JWT_SECRET!))).payload
  }catch(error){
    return false
  }
    
}
export async function checkAuth() {
  try {
    const token = (await cookies()).get('token')?.value
    if (!token) {
      return { isAuthenticated: false }
    }
    const decoded: any = await getToken(token) 
    if (!decoded || !decoded.id) {
      return { isAuthenticated: false }
    }

    return { isAuthenticated: true }
  } catch (error) {
    return { isAuthenticated: false }
  }
}


