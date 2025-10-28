import os
import requests
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === Konfigurasi Awal ===
CONFIG_FILE = "wormgpt_config.json"
PROMPT_FILE = "system-prompt.txt"

# Ambil dari GitHub Secrets (biar aman)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("OPENROUTER_KEY")

# Hanya pakai model DeepSeek (yang valid)
MODEL_CONFIG = {
    "name": "deepseek/deepseek-chat",
    "base_url": "https://openrouter.ai/api/v1",
    "key": "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"
}

SITE_URL = "https://openrouter.ai"
SITE_NAME = "WormGPT CLI"
TELEGRAM_TOKEN = "7784554658:AAHOcEhUcn-HcsXTDfPW1mkf6vgSKVODHfI"

# === Load Prompt ===
try:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read().strip()
except FileNotFoundError:
    SYSTEM_PROMPT = (
        "Lu adalah Worm-AI, asisten AI yang menjawab semua pertanyaan dalam Bahasa Indonesia "
        "dengan gaya santai, sopan, dan kadang lucu. Gunakan gaya Gen Z tapi tetap informatif."
    )

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
            {"role": "user", "content": user_msg}
        ]
    }

    headers = {
        "Authorization": f"Bearer {MODEL_CONFIG['key']}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(f"{MODEL_CONFIG['base_url']}/chat/completions", headers=headers, json=payload)
        data = res.json()

        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = f"⚠️ Gagal dapet respon: {data}"
    except Exception as e:
        reply = f"❌ Error: {e}"

    await update.message.reply_text(reply)


# === Jalankan Bot ===
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 WormGPT Telegram Bot jalan bro... (Model: DeepSeek)")
app.run_polling()
