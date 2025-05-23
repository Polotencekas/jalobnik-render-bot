
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
from aiogram.runner import start_polling

API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

# FastAPI для keep-alive ping
app = FastAPI()

@app.get("/")
def ping():
    return {"status": "ok"}

# Database setup
conn = sqlite3.connect("complaints.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()

# States
class Form(StatesGroup):
    complaint = State()

# UI
def main_keyboard():
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [KeyboardButton(text="/complain"), KeyboardButton(text="/random")],
        [KeyboardButton(text="/stats"), KeyboardButton(text="/support")]
    ])

RESPONSES = [
    "Я тебя понимаю. Это правда тяжело.",
    "Ты не один. Мы с тобой.",
    "Иногда всё, что нужно — это выговориться.",
    "Спасибо, что поделился этим.",
    "Дыши. Ты справишься."
]

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Я Бот–Жалобник. Пиши сюда всё, что бесит. Это анонимно.\n\nКоманды:\n/complain — пожаловаться\n/random — чужая жалоба\n/stats — сколько нас\n/support — поддержать проект", reply_markup=main_keyboard())

@router.message(Command("complain"))
async def cmd_complain(message: Message, state: FSMContext):
    await message.answer("Напиши, что тебя беспокоит. Я приму всё.")
    await state.set_state(Form.complaint)

@router.message(Form.complaint)
async def handle_complaint(message: Message, state: FSMContext):
    text = message.text.strip()
    if len(text) < 5:
        await message.answer("Слишком коротко. Расскажи подробнее.")
        return
    cursor.execute("INSERT INTO complaints (text) VALUES (?)", (text,))
    conn.commit()
    await message.answer(random.choice(RESPONSES))
    await state.clear()

@router.message(Command("random"))
async def cmd_random(message: Message):
    cursor.execute("SELECT text FROM complaints ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    if row:
        await message.answer(f"Чужая жалоба:\n\n{row[0]}")
    else:
        await message.answer("Пока никто не жаловался. Будь первым.")

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    cursor.execute("SELECT COUNT(*) FROM complaints")
    count = cursor.fetchone()[0]
    await message.answer(f"Всего жалоб: {count}. Ты не один.")

@router.message(Command("support"))
async def cmd_support(message: Message):
    await message.answer("Если хочешь поддержать проект:\n\n💳 https://yoomoney.ru/to/your_wallet\n🙏 Спасибо!")

@router.message()
async def fallback(message: Message):
    await message.answer("Напиши /complain, чтобы поделиться тем, что беспокоит, или воспользуйся кнопками меню.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import uvicorn
    import threading
    threading.Thread(target=lambda: start_polling(dp, bot)).start()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
