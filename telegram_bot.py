import os
import requests
import json
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === Konfigurasi Awal ===
CONFIG_FILE = "wormgpt_config.json"
PROMPT_FILE = "system-prompt.txt"

# Ambil dari GitHub Secrets (biar aman)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "Your Token Bot!")
API_KEY = os.getenv("OPENROUTER_KEY", "Your Key Api")

# Hanya pakai model DeepSeek (yang valid)
MODEL_CONFIG = {
    "name": "deepseek/deepseek-chat",
    "base_url": "https://openrouter.ai/api/v1",
    "key": API_KEY,
}

SITE_URL = "https://openrouter.ai"
SITE_NAME = "WormGPT CLI"

# === Handler Telegram ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"Welcome wormGPT {SITE_NAME}.\n\n"
        f"Model wormGPT version deepseekV3\n"
        f"Model AI: {SITE_URL}"
    )
    await update.message.reply_text(msg)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    payload = {
        "model": MODEL_CONFIG["name"],
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
    }

    headers = {
        "Authorization": f"Bearer {MODEL_CONFIG['key']}",
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(
            f"{MODEL_CONFIG['base_url']}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        data = res.json()

        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = f"⚠️ Gagal dapet respon: {data}"
    except Exception as e:
        reply = f"❌ Error: {e}"

    await update.message.reply_text(reply)


# === Jalankan Bot (Mode Webhook) ===
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def main():
    webhook_url = "https://2a78d5ab-c33e-4fa9-ad2f-e164bf64faf1-dev.e1-us-east-azure.choreoapis.dev/default/wormgpt/v1.0/webhook"

    await app.bot.set_webhook(webhook_url)
    print(f"🚀 Webhook set ke: {webhook_url}")

    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=webhook_url,
    )

if __name__ == "__main__":
    try:
        # FIX: biar gak bentrok sama event loop existing
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(main())
        else:
            loop.run_until_complete(main())
    except Exception as e:
        print(f"❌ Gagal jalanin bot: {e}")
