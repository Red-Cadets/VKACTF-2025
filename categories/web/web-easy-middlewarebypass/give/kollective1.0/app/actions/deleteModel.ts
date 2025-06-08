'use server'
import { prisma } from '@/lib/prisma'

export async function deleteModel(id:number) {
  try {
    if(id in [1,2,3,4]){
        throw new Error('Вы не можете удалить эту модель')
    }
    const newModel = await prisma.model.delete({where:{id}})
    return {ok:true}
  } catch (error) {
    throw new Error('Ошибка при удалении модели')
  }
}
