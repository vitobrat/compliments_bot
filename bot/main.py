from aiogram import Bot, Dispatcher
import asyncio
from bot import admin
from bot.handler import handler_commands, handler_messages


async def main() -> None:
    TOKEN = "7260863728:AAGaCtZX8M1L1Pbw6gqy_1XitdyU9noPwn4"
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(admin.router, handler_commands.router, handler_messages.router)

    # Альтернативный вариант регистрации роутеров по одному на строку
    # dp.include_router(questions.router)
    # dp.include_router(different_types.router)

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
