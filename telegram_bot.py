import os
import asyncio
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === Konfigurasi Dasar ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YourTokenHere")
API_KEY = os.getenv("OPENROUTER_KEY", "YourOpenRouterKey")

MODEL_NAME = "deepseek/deepseek-chat"
BASE_URL = "https://openrouter.ai/api/v1"

SYSTEM_PROMPT = (
    "Lu adalah WormGPT, AI yang jawab semua pertanyaan dalam Bahasa Indonesia "
    "dengan gaya Gen Z tapi tetap edukatif dan cerdas."
)

WEBHOOK_URL = "https://2a78d5ab-c33e-4fa9-ad2f-e164bf64faf1-dev.e1-us-east-azure.choreoapis.dev/default/wormgpt/v1.0/webhook"


# === Handler Telegram ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 WormGPT online, bro! Siap bantu lo kapan aja.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload)
        data = res.json()

        reply = data.get("choices", [{}])[0].get("message", {}).get(
            "content", "⚠️ No response from model."
        )
    except Exception as e:
        reply = f"❌ Error: {e}"

    await update.message.reply_text(reply)


# === MAIN PROGRAM ===
async def main():
    print(f"🚀 Setting webhook ke: {WEBHOOK_URL}")

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .build()
import os
import asyncio
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === Konfigurasi Dasar ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YourTokenHere")
API_KEY = os.getenv("OPENROUTER_KEY", "YourOpenRouterKey")

MODEL_NAME = "deepseek/deepseek-chat"
BASE_URL = "https://openrouter.ai/api/v1"

SYSTEM_PROMPT = (
    "Lu adalah WormGPT, AI yang jawab semua pertanyaan dalam Bahasa Indonesia "
    "dengan gaya Gen Z tapi tetap edukatif dan cerdas."
)

WEBHOOK_URL = "https://2a78d5ab-cimport os
import asyncio
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === Konfigurasi Dasar ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YourTokenHere")
API_KEY = os.getenv("OPENROUTER_KEY", "YourOpenRouterKey")

MODEL_NAME = "deepseek/deepseek-chat"
BASE_URL = "https://openrouter.ai/api/v1"

SYSTEM_PROMPT = (
    "Lu adalah WormGPT, AI yang jawab semua pertanyaan dalam Bahasa Indonesia "
    "dengan gaya Gen Z tapi tetap edukatif dan cerdas."
)

WEBHOOK_URL = "https://2a78d5ab-c33e-4fa9-ad2f-e164bf64faf1-dev.e1-us-east-azure.choreoapis.dev/default/wormgpt/v1.0/webhook"


# === Handler Telegram ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 WormGPT online, bro! Siap bantu lo kapan aja.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload)
        data = res.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get(
            "content", "⚠️ No response from model."
        )
    except Exception as e:
        reply = f"❌ Error: {e}"

    await update.message.reply_text(reply)


# === MAIN PROGRAM ===
async def main():
    print(f"🚀 Setting webhook ke: {WEBHOOK_URL}")

    # Buat instance aplikasi Telegram bot
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Tambahkan handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Set webhook URL ke bot Telegram
    await app.bot.set_webhook(WEBHOOK_URL)

    # Jalankan webhook listener
    await app.initialize()
    await app.start()
    print("✅ Bot is now running in webhook mode...")

    # Tunggu webhook berjalan (server aktif)
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        # Kalau loop udah jalan (kayak di Choreo environment)
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
