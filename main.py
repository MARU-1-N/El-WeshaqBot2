from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from datetime import datetime, timedelta
import re

BOT_TOKEN = "7972999569:AAHpcZ-JxaKfF0XMgr-ZWn94HvTj85HCI8I"
CHANNEL_USERNAME = "@TeamElWeshaq"

# حالات المستخدمين
user_states = {}

# دالة الوقت
def is_recent(msg_date):
    return msg_date >= datetime.utcnow() - timedelta(minutes=5)

# دالة البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔍 البحث عن OTP", callback_data="search_otp")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 مرحبًا بك في بوت El-Weshaq!\nاختر أمرًا من الأسفل:", reply_markup=reply_markup)

# التعامل مع الزر
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user_states[user_id] = "awaiting_otp_digits"
    await query.message.reply_text("🧠 أرسل آخر **4 أرقام فقط** من الرقم (مثلاً: 1234):")

# استقبال رسالة الأرقام
async def handle_number_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_states.get(user_id) != "awaiting_otp_digits":
        return

    digits = update.message.text.strip()
    if not re.fullmatch(r"\d{4}", digits):
        await update.message.reply_text("❗ أرسل فقط **4 أرقام صحيحة** (مثال: 1234)")
        return

    await update.message.reply_text(f"🔎 جاري البحث عن الرسائل التي تحتوي الرقم {digits} في آخر 5 دقائق...")

    found = False
    async for msg in context.bot.get_chat_history(CHANNEL_USERNAME, limit=100):
        if not is_recent(msg.date):
            break
        if msg.text and digits in msg.text:
            await update.message.reply_text(f"📨 تم العثور على:\n\n{msg.text}")
            found = True
            break

    if not found:
        await update.message.reply_text("❌ لم يتم العثور على أي نتيجة خلال آخر 5 دقائق.")
    user_states.pop(user_id, None)

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number_message))
    print("✅ البوت يعمل الآن...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
