import requests
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === Konfigurasi Awal ===
CONFIG_FILE = "wormgpt_config.json"
PROMPT_FILE = "system-prompt.txt"

DEFAULT_API_KEY = "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"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "cohere/command-r-plus:free"
SITE_URL = "https://openrouter.ai"
SITE_NAME = "WormGPT CLI"

TELEGRAM_TOKEN = "7784554658:AAHOcEhUcn-HcsXTDfPW1mkf6vgSKVODHfI"

# === Load Config ===
try:
    with open(CONFIG_FILE, "r") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    CONFIG = {
        "api_key": DEFAULT_API_KEY,
        "base_url": DEFAULT_BASE_URL,
        "model": DEFAULT_MODEL
    }

API_KEY = CONFIG.get("api_key", DEFAULT_API_KEY)
API_URL = CONFIG.get("base_url", DEFAULT_BASE_URL) + "/chat/completions"
MODEL = CONFIG.get("model", DEFAULT_MODEL)

# === Load System Prompt ===
try:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read().strip()
except FileNotFoundError:
    SYSTEM_PROMPT = (
        "Kamu adalah Worm-AI, asisten AI yang menjawab semua pertanyaan dalam Bahasa Indonesia "
        "dengan gaya santai, sopan, dan kadang lucu. Gunakan gaya Gen Z tapi tetap informatif."
    )

# === Telegram Bot Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"Yo bro 😎! Ini {SITE_NAME}.\n\n"
        f"Aku siap bantu lo 24 jam nonstop 💪\n"
        f"Repo: {SITE_URL}"
    )
    await update.message.reply_text(msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload)
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

print("🚀 WormGPT Telegram Bot jalan bro...")
app.run_polling()
