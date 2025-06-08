import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

async function main() {

  await prisma.model.createMany({
    data: [
      { name: 'ЭМ-1', combat: false },
      { name: 'БТ-4', combat: false },
      { name: 'Т-73', combat: true },
      { name: 'РП-70', combat: false },
    ],
    skipDuplicates:true
  });
  await prisma.order.createMany({
    data: [
      { message: 'Перехватить шпионов модели ЭМ-1', modelId: 1 },
      { message: 'Сканирование территории для модели ЭМ-1', modelId: 1 },
      { message: 'Уничтожить вражеские силы для модели БТ-4', modelId: 2 },
      { message: 'Поддержка операций для модели БТ-4', modelId: 2 },
      { message: 'vka{DUMMY}', modelId: 3 },
      { message: 'Защита объекта для модели Т-73', modelId: 3 },
      { message: 'Отправить на патрулирование для модели РП-70', modelId: 4 },
      { message: 'Собрать разведданные для модели РП-70', modelId: 4 },
    ],
    skipDuplicates:true
  });
}

main()
  .catch(e => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
