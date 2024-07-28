import random
import asyncio
from asyncio import sleep

import aiofiles
from aiogram import Bot

from aiosqlitedatabase.database import get_all_users_id_with_send_mode

file_path = "bot/compliments/compliments.txt"


class Compliment:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._compliments = []
            self.file_path = file_path
            self._initialized = True

    async def load_compliments(self) -> None:
        print("Пиздец")
        if not self._compliments:  # Проверка, чтобы загрузить комплименты только один раз
            async with aiofiles.open(self.file_path, 'r', encoding='utf-8') as file:
                compliments = await file.readlines()
            compliment = ""
            for line in compliments:
                if line == "$$\n":
                    self._compliments.append(compliment.strip())
                    compliment = ""
                else:
                    compliment += line
            if compliment:  # Добавить последний комплимент, если он не пуст
                self._compliments.append(compliment.strip())

    async def send_compliment(self, user_id: int, bot):
        if not self._compliments:
            await self.load_compliments()
        compliment = random.choice(self._compliments)
        try:
            await bot.send_message(user_id, compliment)
            print(user_id, compliment)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")


# Пример использования
async def run_send_compliment(bot: Bot, minute: int):
    compliment = Compliment()
    await compliment.load_compliments()
    while True:
        users_id = [id[0] for id in await get_all_users_id_with_send_mode()]
        for id in users_id:
            await compliment.send_compliment(id, bot)
            await asyncio.sleep(0.3)
        await asyncio.sleep(minute * 60)
