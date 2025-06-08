'use server'
import { prisma } from '@/lib/prisma'
import { cookies } from 'next/headers'
import { getToken } from './auth'


export async function getOrders() {
  try {
    const token = (await cookies()).get('token')?.value
    
    if (!token) {
        
        return { error: 'Токен не найден' }
    }

    const decoded: any = await getToken(token)
    const modelId = decoded.modelId
    if(!modelId) return { error: 'Неправильная модель' }
    if(!await prisma.model.findFirst({where:{id:modelId}}))return { error: 'Неправильная модель' }
    const orders = await prisma.order.findMany({
      where: {
        modelId: modelId
      },
      include: {
        model: {
          select: { name: true }
        }
      }
    })

    return orders
  } catch (error) {
    throw { error: 'Произошла ошибка при получении приказов' }
  }
}
