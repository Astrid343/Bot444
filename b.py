import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# --- ЛОГИ ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

# --- КЛЮЧИ ---
TELEGRAM_BOT_TOKEN = "7942858083:AAG1E_upeUZayYi33OfA6y9eGSyo3-dwJc4"
OPENROUTER_API_KEY = "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"

# --- OpenRouter КЛИЕНТ ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# --- GPT-ФУНКЦИЯ ---
async def generate_response(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        logger.info(f"📦 Ответ от OpenRouter: {completion}")

        if not completion or not completion.choices:
            return "⚠️ Модель не вернула ответ. Проверь ключ и модель."

        content = completion.choices[0].message.content
        return content.strip() if content else "⚠️ Пустой ответ от модели."

    except Exception as e:
        logger.error(f"❌ Ошибка генерации: {e}")
        return f"❌ Ошибка генерации ответа: {e}"

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Напиши мне что-нибудь.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"📥 Сообщение: {user_message}")
    reply = await generate_response(user_message)
    await update.message.reply_text(reply)

# --- ЗАПУСК ---
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Бот успешно запущен.")
    app.run_polling()

if name == "main":
    main()