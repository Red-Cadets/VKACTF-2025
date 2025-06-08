'use server'
import { prisma } from '@/lib/prisma'
import { cookies } from 'next/headers'
import bcrypt from 'bcrypt'
import { signToken } from './auth'

const saltOrRounds = 10 
const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;

export async function loginRobot({ name, password }: { name: string, password: string }) {
    try {
      const robot = await prisma.robot.findFirst({ where: { name } })
      if (!robot) {
        return { error: 'Такого робота не существует' }
      }
  
      const isValid = await bcrypt.compare(password, robot.password)
      if (!isValid) {
        return { error: 'Неверный пароль' }
      }
  
      const payload = {
        id: robot.id,
        name: String(robot.name),
        modelId: robot.modelId
      }
  
      const token = await signToken(payload)
  
      const cookie = cookies()
      ;(await cookie).set('token', token, { httpOnly: true, secure: process.env.NODE_ENV === 'production', path: '/' })
  
      return {
        result: 'success',
        data: payload,
        token
      }
    } catch (error) {
      console.error(error)
      return { error: 'Произошла ошибка при авторизации' }
    }
}

export async function registerRobot({ name, password, repass, modelId }: { name: string, password: string, repass:string, modelId: number }) {

  try {
    const existingRobot = await prisma.robot.findFirst({ where: { name } })
    if (existingRobot) {
      return { error: 'Робот с таким логином уже существует' }
    }
    if (!passwordRegex.test(password)) {
      return { error: 'Пароль должен содержать минимум 8 символов, включая заглавную, строчную букву, цифру и спецсимвол.' };
    }
    if (password !== repass) {
      return { error: 'Пароли не совпадают' }
    }

    const model = await prisma.model.findFirst({ where: { id: modelId } })
    if (!model || model.combat) {
      return { error: 'Вы не можете зарегистрироваться как боевой робот. Их регистрирует администратор' }
    }

    const hashedPassword = await bcrypt.hash(password, saltOrRounds)

    const newRobot = await prisma.robot.create({
      data: {
        name,
        password: hashedPassword,
        modelId
      }
    })

    const payload = {
      id: newRobot.id,
      name: String(newRobot.name),
      modelId: newRobot.modelId
    }

    const token = await signToken(payload)

    const cookie = cookies()
    ;(await cookie).set('token', token, { httpOnly: true, secure: process.env.NODE_ENV === 'production', path: '/' })

    return {
      result: 'success',
      data: payload,
      token
    }
  } catch (error) {
    return { error: 'Произошла ошибка при регистрации' }
  }

}
