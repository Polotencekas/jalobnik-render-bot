import os
import random
import logging
import sqlite3

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types, start_polling
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram import Router

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Ваши обработчики и логика бота здесь

if __name__ == "__main__":
    start_polling(dp)
