'use server'
import { prisma } from '@/lib/prisma'

export async function getAllRobots() {
  try {
    const robots = await prisma.robot.findMany({
      include: {
        model: {
          select: {
            name: true,
          },
        },
      },
    })

    return robots
  } catch (error) {
    console.error('Ошибка при получении роботов:', error)
    return {error: 'Не удалось получить роботов'}
  }
}
