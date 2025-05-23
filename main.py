import os
import random
import logging
import sqlite3

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram import Router
from aiogram import executor  # Используем executor для запуска

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

router = Router()
dp.include_router(router)

# Пример хендлера команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Бот запущен и готов к работе!")

# Пример хендлера обычной команды /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Вот список доступных команд: /start /help")

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
