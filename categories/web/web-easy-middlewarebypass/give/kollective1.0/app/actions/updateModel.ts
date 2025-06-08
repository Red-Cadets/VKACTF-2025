'use server'
import { prisma } from '@/lib/prisma'

export async function updateModel(id:number, name:string) {
  try {
    if(id in [1,2,3,4]){
        throw new Error('Вы не можете изменить эту модель')
    }
    const newModel = await prisma.model.update({where:{id}, data:{name}})
    return newModel
  } catch (error) {
    throw new Error('Ошибка при обновлении модели')
  }
}
