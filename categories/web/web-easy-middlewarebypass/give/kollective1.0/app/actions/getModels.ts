'use server'
import { prisma } from '@/lib/prisma'

export async function getAllModels() {
  try {
    const models = await prisma.model.findMany({
      include: {
        robots: {
          select: {
            name: true,
          },
        },
      },
    })
    return models
  } catch (error) {
    console.error('Ошибка при получении моделей:', error)
    throw new Error('Ошибка при получении модели')
  }
}
