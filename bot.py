import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import date

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')

def days_until_new_year():
    """Вычисляет количество дней до Нового Года"""
    # ЖЕСТКО задаем количество дней
    days = 46  # ← 16 ноября 2024 → 1 января 2025
    print(f"🔴 ДЕБАГ: ЖЕСТКО ЗАДАНО: {days} дней до НГ")
    return days
    print(f"🔴 ДЕБАГ: Сегодня {today}, До 1 января {next_year}: {days} дней")
    return days

def get_new_year_info():
    """Возвращает красивую информацию о Новом Годе"""
    days = days_until_new_year()
    
    if days == 0:
        return "🎉 С НОВЫМ ГОДОМ! 🎉\nПусть все мечты сбудутся!"
    elif days == 1:
        return "Завтра Новый Год! 🎄\nУже завтра!"
    elif days < 10:
        return f"🎄 Совсем скоро! До Нового Года: {days} дней!"
    elif days < 30:
        return f"❄️ Уже близко! До Нового Года: {days} дней"
    else:
        return f"⏳ До Нового Года: {days} дней"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.message.from_user
    logger.info(f"Пользователь {user.first_name} запустил бота")
    
    # Создаем клавиатуру
    keyboard = [
        ['🎄 Узнать сколько дней до НГ'],
        ['❓ Помощь', '⭐ О боте']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_text = f"""
Привет, {user.first_name}! 👋

Я - бот отсчета до Нового Года! 🎅

Выбери действие ниже или напиши /help для помощи.
    """
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
📖 **Помощь по боту:**

/start - Запустить бота
/help - Показать эту помощь
/days - Узнать сколько дней до НГ

Или просто используй кнопки ниже! 🎄
    """
    await update.message.reply_text(help_text)

async def days_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /days"""
    days = days_until_new_year()
    message = get_new_year_info()
    await update.message.reply_text(message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text
    user = update.message.from_user
    
    if text == '🎄 Узнать сколько дней до НГ':
        message = get_new_year_info()
        await update.message.reply_text(message)
        
    elif text == '❓ Помощь':
        await help_command(update, context)
        
    elif text == '⭐ О боте':
        about_text = """
🤖 **О боте:**
        
Бот отсчета до Нового Года 2025!
        
Разработан с ❤️ для создания праздничного настроения!
        
Каждый день - на шаг ближе к чуду! 🎅
        """
        await update.message.reply_text(about_text)
        
    else:
        # Если сообщение не распознано
        await update.message.reply_text(
            "Не понял тебя... 😊\n"
            "Используй кнопки или команду /help для помощи."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")

def main():
    """Основная функция запуска бота"""
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN не задан! Добавьте его в переменные окружения.")
    
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("days", days_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    print("✅ Бот запущен и готов к работе!")
    print("🔄 Ожидаем сообщения...")
    application.run_polling()

if __name__ == "__main__":
    main()
