'use server'

import { prisma } from '@/lib/prisma'
import { cookies } from 'next/headers'
import { getToken, signToken } from './auth' 

export async function updateBio(bio: string, modelId: number) {
  try {
    const token = (await cookies()).get('token')?.value
    
    if (!token) {
      return { error: 'Токен не найден' }
    }

    const decoded: any = await getToken(token)
    if (!decoded || !decoded.id) {
      return { error: 'Недопустимый токен' }
    }

    const id = decoded.id
    let updatedModelId = modelId || decoded.modelId

    if (modelId && modelId !== decoded.modelId) {
      const model = await prisma.model.findFirst({ where: { id: modelId } })
      if (!model || model.combat) {
        return { error: 'Вы не можете выбрать эту модель, это боевой робот. Их регистрирует администратор' }
      }
      updatedModelId = modelId 
    }

    const robot = await prisma.robot.update({
      where: {
        id,
      },
      data: {
        bio,
        modelId: updatedModelId
      },
      select: {
        name: true,
        bio: true,
        model: {
          select: { name: true }
        }
      }
    })

    if (!robot) return { error: 'Ошибка изменения профиля' }

    if (updatedModelId !== decoded.modelId) {
      const newToken = await signToken({
        id: decoded.id,
        name: decoded.name,
        modelId: updatedModelId
      })

      const cookieStore = cookies()
      ;(await cookieStore).set('token', newToken)
    }

    return robot
  } catch (error) {
    console.log(error)
    return { error: 'Ошибка изменения профиля' }
  }
}
