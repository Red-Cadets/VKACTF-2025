'use server'
import { prisma } from '@/lib/prisma'

export async function addModel(name: string) {
  try {
    const newModel = await prisma.model.create({
      data: {
        name: name,
      },
      select:{
        id:true,
        name:true,
        combat:true,
        robots:{
          select:{
            name:true
          }
        }
      }
    })
    return newModel
  } catch (error) {
    throw new Error('Ошибка при добавлении модели')
  }
}
