'use server'
import { prisma } from '@/lib/prisma'

export async function processFile(file: string) {


  const queries = file.split(';').filter(q => q.trim().length > 0)
  let result: string = ''

  for (const query of queries) {
    try {
      if (!query.trim().toUpperCase().startsWith('INSERT')) {
        continue;
      }
      const queryRes = await prisma.$queryRawUnsafe(query)
      result += JSON.stringify(queryRes, null, 2)
    } catch (error) {
      throw new Error(`Ошибка при выполнении запроса: ${query}`)
    }
  }
  return { status: 'Ok' }

}
