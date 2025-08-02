from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler from datetime import datetime, timedelta import asyncio

توكن البوت

BOT_TOKEN = "7972999569:AAHpcZ-JxaKfF0XMgr-ZWn94HvTj85HCI8I"

معرف القناة المستهدفة

TARGET_CHAT = "@TeamElWeshaq"

التخزين المؤقت للرسائل الأخيرة

last_messages = []

قائمة انتظار البحث لكل مستخدم

user_search_mode = {}

وظيفة لتخزين الرسائل من القناة

async def cache_group_messages(app): last_messages.clear() async for msg in app.get_chat_history(TARGET_CHAT, limit=100): if msg.date > datetime.utcnow() - timedelta(minutes=5): last_messages.append(msg) else: break

أمر /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [ [InlineKeyboardButton("🔍 البحث عن OTP", callback_data="search_otp")], ] reply_markup = InlineKeyboardMarkup(keyboard) await update.message.reply_text("مرحبًا بك في بوت Team_ElWeshaq! اختر من القائمة:", reply_markup=reply_markup)

التعامل مع ضغط الأزرار

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer()

if query.data == "search_otp":
    user_search_mode[query.from_user.id] = True
    await query.edit_message_text("📨 من فضلك أرسل الرقم الذي يحتوي على نجوم:")

استقبال الرسائل بعد اختيار البحث

async def handle_user_msg(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id text = update.message.text.strip()

if user_id in user_search_mode and user_search_mode[user_id]:
    del user_search_mode[user_id]

    # استخراج آخر 4 أرقام
    import re
    matches = re.findall(r'(\d{4})\s*$', text)
    if not matches:
        await update.message.reply_text("⚠️ لم يتم العثور على 4 أرقام في الرسالة. حاول مجددًا.")
        return

    last_four = matches[0]

    # البحث في الرسائل المخزنة
    for msg in last_messages:
        if last_four in msg.text_html:
            await update.message.reply_html(f"📩 تم العثور على الرسالة:

{msg.text_html}") return

await update.message.reply_text("❌ لم يتم العثور على رسالة تحتوي الرقم خلال آخر 5 دقائق.")
else:
    await update.message.reply_text("🤖 أرسل /start لاستخدام القائمة.")

بدء التطبيق

async def main(): app = ApplicationBuilder().token(BOT_TOKEN).build()

# تحديث الكاش كل دقيقتين
async def refresh_cache(context: ContextTypes.DEFAULT_TYPE):
    await cache_group_messages(app)

app.job_queue.run_repeating(refresh_cache, interval=120, first=0)

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_msg))

print("🤖 البوت يعمل...")
await app.run_polling()

if name == 'main': asyncio.run(main())

