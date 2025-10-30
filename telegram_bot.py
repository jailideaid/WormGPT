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

import os
import json
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === CONFIGURATION ===
CONFIG_FILE = "wormgpt_config.json"
PROMPT_FILE = "system-prompt.txt"

# Ambil token dan key dari environment (atau bisa langsung ditulis manual)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "Your Token Bot!")
API_KEY = os.getenv("OPENROUTER_KEY", "Your Key Api")

# Model DeepSeek yang valid
MODEL_CONFIG = {
    "name": "deepseek/deepseek-chat",
    "base_url": "https://openrouter.ai/api/v1",
    "key": API_KEY
}

SITE_URL = "https://openrouter.ai"
SITE_NAME = "WormGPT CLI"

# === LOAD SYSTEM PROMPT ===
if os.path.exists(PROMPT_FILE):
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read().strip()
else:
    SYSTEM_PROMPT = "You are WormGPT running DeepSeek model."


# === HANDLER: /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"👋 Welcome to {SITE_NAME}!\n\n"
        f"🤖 Model: DeepSeek (wormGPT version)\n"
        f"🌐 Source: {SITE_URL}"
    )
    await update.message.reply_text(msg)


# === HANDLER: MESSAGE ===
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
        res = requests.post(
            f"{MODEL_CONFIG['base_url']}/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = res.json()

        if "choices" in data and len(data["choices"]) > 0:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = f"⚠️ Gagal dapet respon: {json.dumps(data, indent=2)}"

    except Exception as e:
        reply = f"❌ Error: {e}"

    await update.message.reply_text(reply)


# === MAIN TELEGRAM BOT ===
def main():
    print("🚀 WormGPT Telegram Running... (Model: DeepSeek)")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
