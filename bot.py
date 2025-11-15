import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get('BOT_TOKEN')

def days_until_new_year():
    from datetime import date
    today = date.today()
    next_year = today.year + 1
    new_year = date(next_year, 1, 1)
    days = (new_year - today).days
    print(f"🔴 АВТОМАТ: Сегодня {today}, До НГ: {days} дней")
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
    app.run_polling()

if __name__ == "__main__":
    main()
