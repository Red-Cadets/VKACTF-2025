'use server'
import { prisma } from '@/lib/prisma'

export async function getAllOrders() {
  try {
    const orders = await prisma.order.findMany({
        where:{
            model:{
                combat:false
            }
        },
        include:{
            model:{
                select:{
                  id:true,
                    name:true
                }
            }
        }
    })
    return orders
  } catch (error) {
    console.error('Ошибка при получении приказов:', error)
    throw new Error('Ошибка при получении приказов')
  }
}
