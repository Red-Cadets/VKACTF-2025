'use server'

import { prisma } from '@/lib/prisma'
import { cookies } from 'next/headers'
import bcrypt from 'bcrypt'
import { signToken } from './auth'

const saltOrRounds = 10

export async function adminLogin({ login, password }: { login: string, password: string }) {
  try {
    const user = await prisma.user.findFirst({ where: { login } })
    if (!user) {
      return { error: 'Не удалось авторизоваться' }
    }

    const isValid = await bcrypt.compare(password, user.password)
    if (!isValid) {
      return { error: 'Не удалось авторизоваться' }
    }

    const payload = {
      id: user.id,
      login: String(user.login),
      admin: true
    }

    const token = await signToken(payload)

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

export async function adminRegister({ login, password, repass }: { login: string, password: string, repass: string }) {

  try {
    const existingRobot = await prisma.user.findFirst({ where: { login } })
    if (existingRobot) {
      return { error: 'User с таким логином уже существует' }
    }

    if (password !== repass) {
      return { error: 'Пароли не совпадают' }
    }

    const hashedPassword = await bcrypt.hash(password, saltOrRounds)

    const user = await prisma.user.create({
      data: {
        login,
        password: hashedPassword
      }
    })

    const payload = {
      id: user.id,
      login: String(user.login),
      admin: true
    }

    const token = await signToken(payload)

    const cookie = cookies()
      ; (await cookie).set('token', token, { httpOnly: true, secure: process.env.NODE_ENV === 'production', path: '/' })

    return {
      result: 'success',
      data: payload,
      token
    }
  } catch (error) {
    console.error(error)
    return { error: 'Произошла ошибка при регистрации' }
  }

}
