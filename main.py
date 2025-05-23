import os
import random
import logging
import sqlite3

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import CommandStart, Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=["start"])
async def cmd_start(message: Message):
    await message.answer("Бот запущен и готов к работе!")

@dp.message_handler(commands=["help"])
async def cmd_help(message: Message):
    await message.answer("Вот список доступных команд: /start /help")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
