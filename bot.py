import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import date

BOT_TOKEN = os.environ.get('BOT_TOKEN')

def days_until_new_year():
    from datetime import date
    start_date = date(2025, 11, 17)
    real_today = date.today()
    days_passed = (real_today - start_date).days
    days_left = 45 - days_passed
    print(f"🎯 Авто-отсчет: {days_left} дней до НГ")
    return days_left

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
