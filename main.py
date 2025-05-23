import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram import Router
from aiogram.runner import start_polling  # <- правильно импортируем polling

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

router = Router()
dp.include_router(router)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Бот запущен и готов к работе!")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Вот список доступных команд: /start /help")


if __name__ == "__main__":
    start_polling(dp, skip_updates=True)
