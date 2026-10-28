import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from dotenv import load_dotenv

# Загружаем настройки из файла .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Настраиваем сообщения об ошибках
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаём бота и диспетчер
dp = Dispatcher()

# Советы и мотивация
MOTIVATION = [
    "🌱 Каждый маленький шаг приближает тебя к цели!",
    "💪 Ошибки — это часть обучения. Не останавливайся!",
    "🚀 Начни сегодня, даже если можешь сделать совсем немного.",
    "✨ Ты не обязана знать всё сразу. Учись постепенно!",
]

STUDY_TIPS = [
    "📚 Учись 25 минут, затем отдыхай 5 минут.",
    "📝 Записывай главные мысли урока своими словами.",
    "📵 Убери телефон на время занятий.",
    "🎯 Сначала выполни одну важную задачу, потом переходи к следующей.",
]


# Создаём кнопки меню
def main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💪 Мотивация",
                    callback_data="motivation",
                ),
                InlineKeyboardButton(
                    text="📚 Совет для учёбы",
                    callback_data="study",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📅 План на 25 минут",
                    callback_data="plan",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❓ Помощь",
                    callback_data="help",
                ),
            ],
        ]
    )


# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    name = user.first_name if user else "друг"

    text = (
        f"Привет, {name}! 👋\n\n"
        "Я CLRGIFBOT — твой помощник для учёбы и продуктивности. 🤖\n\n"
        "✨ Что я умею:\n"
        "💪 Поднимать настроение\n"
        "📚 Давать советы для учёбы\n"
        "📅 Помогать планировать занятия\n\n"
        "Выбери действие в меню ниже!"
    )

    await message.answer(text, reply_markup=main_keyboard())


# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📖 Справочник NobiBot\n\n"
        "/start — открыть главное меню\n"
        "/help — список команд\n"
        "/motivation — получить мотивацию\n"
        "/study — получить совет для учёбы\n"
        "/plan — план занятий на 25 минут\n\n"
        "Также ты можешь пользоваться кнопками меню. ✨"
    )

    await message.answer(text, reply_markup=main_keyboard())


# Команда /motivation
@dp.message(Command("motivation"))
async def cmd_motivation(message: Message):
    await message.answer(random.choice(MOTIVATION))


# Команда /study
@dp.message(Command("study"))
async def cmd_study(message: Message):
    await message.answer(random.choice(STUDY_TIPS))


# Команда /plan
@dp.message(Command("plan"))
async def cmd_plan(message: Message):
    text = (
        "📅 Твой план на 25 минут\n\n"
        "1️⃣ Выбери одну задачу.\n"
        "2️⃣ Убери отвлекающие уведомления.\n"
        "3️⃣ Работай над задачей 25 минут.\n"
        "4️⃣ Проверь результат.\n"
        "5️⃣ Отдохни 5 минут. ☕\n\n"
        "Главное — начать! 🚀"
    )
    await message.answer(text)


# Обрабатываем нажатия кнопок
@dp.callback_query(F.data.in_({"motivation", "study", "plan", "help"}))
async def button_handler(callback: CallbackQuery):
    await callback.answer()

    if callback.data == "motivation":
        text = random.choice(MOTIVATION)
    elif callback.data == "study":
        text = random.choice(STUDY_TIPS)
    elif callback.data == "plan":
        text = (
            "📅 План на 25 минут\n\n"
            "1️⃣ Выбери одну задачу.\n"
            "2️⃣ Работай 25 минут.\n"
            "3️⃣ Проверь результат.\n"
            "4️⃣ Отдохни 5 минут. ☕"
        )
    else:
        text = (
            "❓ Команды CLRGIFBOT\n\n"
            "/start — главное меню\n"
            "/help — помощь\n"
            "/motivation — мотивация\n"
            "/study — совет для учёбы\n"
            "/plan — план занятий"
        )

    if callback.message:
        await callback.message.answer(text, reply_markup=main_keyboard())


# Запускаем программу
async def main():
    if not TOKEN:
        raise RuntimeError(
            "Не найден BOT_TOKEN! Проверь файл .env рядом с bot.py."
        )

    bot = Bot(token=TOKEN)

    try:
        me = await bot.get_me()
        logger.info("Бот запущен: @%s", me.username)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("CLRGIFBOT остановлен.")
