'use server'
import { prisma } from '@/lib/prisma'
import { cookies } from 'next/headers'
import { getToken } from './auth'


export async function getRobot() {
  try {
    const token = (await cookies()).get('token')?.value
    
    if (!token) {
        
        return { error: 'Токен не найден' }
    }

    const decoded: any = getToken(token)
    const id = decoded.id

    const robot = await prisma.robot.findFirst({
      where: {
        id
      },
      select: {
        name:true,
        bio:true,
        modelId:true,
        model: {
          select: { name: true }
        }
      }
    })
    if(!robot) return { error: 'Ошибка получения профиля' }
    return robot
  } catch (error) {
    return { error: 'Ошибка получения профиля' }
  }
}
