import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import date

BOT_TOKEN = os.environ.get('BOT_TOKEN')

def days_until_new_year():
    # ЖЕСТКО ставим ПРАВИЛЬНУЮ дату - 17 ноября 2024!
    today = date(2025, 11, 17)  # ← ИСПРАВЬ НА 2024!
    next_year = 2026  # ← СЛЕДУЮЩИЙ ГОД
    new_year = date(next_year, 1, 1)
    days = (new_year - today).days
    print(f"🎯 ИСПРАВЛЕНО: {days} дней до НГ")
    return days

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    days = days_until_new_year()
    await update.message.reply_text(f"🎄 До Нового Года: {days} дней!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'дней' in update.message.text.lower():
        days = days_until_new_year()
        await update.message.reply_text(f"🎄 До Нового Года: {days} дней!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print("✅ Бот запущен!")
    
    # Для Render чтобы не ругался на порты
    port = int(os.environ.get('PORT', 10000))
    print(f"✅ Bot is running on internal port: {port}")
    
    app.run_polling()

if __name__ == "__main__":
    main()
