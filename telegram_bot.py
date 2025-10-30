import os
import threading
import time
import requests
import json
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio

# === Konfigurasi Awal ===
CONFIG_FILE = "wormgpt_config.json"
PROMPT_FILE = "system-prompt.txt"

MODEL_CONFIG = {
    "name": "deepseek/deepseek-chat",
    "base_url": "https://openrouter.ai/api/v1",
    "key": "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"
}

SITE_URL = "https://openrouter.ai"
SITE_NAME = "WormGPT CLI"

# === Token & Webhook ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "7784554658:AAHOcEhUcn-HcsXTDfPW1mkf6vgSKVODHfI"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or "https://2a78d5ab-c33e-4fa9-ad2f-e164bf64faf1-dev.e1-us-east-azure.choreoapis.dev/default/wormgpt/v1.0/webhook"
PORT = int(os.getenv("PORT", 8000))  # 🔥 ubah ke 8000 biar cocok dengan Choreo

# === Load Prompt ===
try:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read().strip()
except FileNotFoundError:
    SYSTEM_PROMPT = (
        "Lu adalah Worm-AI, asisten AI yang menjawab semua pertanyaan dalam Bahasa Indonesia "
        "dengan gaya santai, sopan, dan kadang lucu. Gunakan gaya Gen Z tapi tetap informatif."
    )

# === Setup Flask ===
app = Flask(__name__)

# === Setup Telegram ===
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

# === Handler Telegram ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"Welcome wormGPT {SITE_NAME}.\n\n"
        f"Model wormGPT version DeepSeekV3\n"
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

telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# === Flask Webhook Route ===
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put_nowait(update)
    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return "💡 WormGPT Flask server is alive!", 200

# === Keep Alive ===
def keep_alive():
    while True:
        try:
            requests.get(WEBHOOK_URL.replace("/webhook", ""))  # ping ke root aja
            print("💓 Ping sent to Choreo.")
        except Exception as e:
            print("⚠️ Gagal ping:", e)
        time.sleep(300)

# === Jalankan Bot dan Flask ===
async def set_webhook():
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook Telegram berhasil diset!")

def run_bot():
    asyncio.run(set_webhook())

def run_flask():
    print(f"🌐 Flask webhook aktif di port {PORT}")
    app.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    print("🔥 WormGPT Telegram Bot jalan bro... (Mode: Webhook)")
    threading.Thread(target=keep_alive, daemon=True).start()
    threading.Thread(target=run_bot, daemon=True).start()
    run_flask()
