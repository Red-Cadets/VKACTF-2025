'use server'
import { prisma } from '@/lib/prisma'

export async function addOrder(message: string, modelId: number) {
  try {
    const newModel = await prisma.order.create({
      data: {
        message,
        modelId
      }
    })
    return newModel
  } catch (error) {
    throw new Error('Ошибка при добавлении приказа')
  }
}
