# main.py
# Главный скрипт для запуска бота

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import config
import database

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start."""
    update.message.reply_text("Привет! Я ваш Telegram-бот. Чем могу помочь?")

async def main():
    """Основной запуск бота."""
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))

    # Запуск бота
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
