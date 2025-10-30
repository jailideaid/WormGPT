import os
import requests
import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

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
TELEGRAM_TOKEN = "7784554658:AAHOcEhUcn-HcsXTDfPW1mkf6vgSKVODHfI"

# === URL Webhook dari Choreo ===
WEBHOOK_URL = "https://2a78d5ab-c33e-4fa9-ad2f-e164bf64faf1-dev.e1-us-east-azure.choreoapis.dev/default/wormgpt/v1.0"
ACCESS_TOKEN = """eyJraWQiOiJnYXRld2F5X2NlcnRpZmljYXRlX2FsaWFzIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJjZGYyNTg2MS01YTYyLTRlM2UtYWY1Yi02MmNjNDEzYTJlZThAY2FyYm9uLnN1cGVyIiwiYXVkIjoiY2hvcmVvOmRlcGxveW1lbnQ6c2FuZGJveCIsIm9yZ2FuaXphdGlvbiI6eyJ1dWlkIjoiMmE3OGQ1YWItYzMzZS00ZmE5LWFkMmYtZTE2NGJmNjRmYWYxIn0sImlzcyI6Imh0dHBzOlwvXC9zdHMuY2hvcmVvLmRldjo0NDNcL2FwaVwvYW1cL3B1Ymxpc2hlclwvdjJcL2FwaXNcL2ludGVybmFsLWtleSIsImtleXR5cGUiOiJTQU5EQk9YIiwic3Vic2NyaWJlZEFQSXMiOlt7InN1YnNjcmliZXJUZW5hbnREb21haW4iOm51bGwsIm5hbWUiOiJ3b3JtZ3B0IC0gZGVmYXVsdC1lbmRwb2ludCIsImNvbnRleHQiOiJcLzJhNzhkNWFiLWMzM2UtNGZhOS1hZDJmLWUxNjRiZjY0ZmFmMVwvZGVmYXVsdFwvd29ybWdwdFwvdjEuMCIsInB1Ymxpc2hlciI6ImNob3Jlb19wcm9kX2FwaW1fYWRtaW4iLCJ2ZXJzaW9uIjoidjEuMCIsInN1YnNjcmlwdGlvblRpZXIiOm51bGx9XSwiZXhwIjoxNzYxODA2NDIwLCJ0b2tlbl90eXBlIjoiSW50ZXJuYWxLZXkiLCJpYXQiOjE3NjE4MDU4MjAsImp0aSI6IjQwMmU2NjI5LTNhMDYtNDEyZC1iYTMyLWE2N2NiZjA2Y2UxMiJ9.iV5y1XZPw_czkRRzJOo0Gp4VN4lHbmA71mGPiRYcTGH_I7yh95rB_M474Iv06wpSQBtTwlW6QuSSLYcFeBQ3KzXYHl3rnmJxAdXFD5-iYpCWHxUQyTEuNz2Jb-4y4c0kN-dJ-r1x1nSptd8k6JPcAuOMkGmTziurhu2fHXS333z77qe3Kui8bfaKUquJUdzhT66O-DbZebtAsBCutb0K2bLx5hZVDQycb8JC0yjOcSaNdH6OI_WjKlRdkDVB4LNpLHtoWRq4TSQLkTWKP37RanWLA30-1qLblkPIaSQ5xatzx0bKeRSq5Eh3XmqRRqZh7Pcd_lyTEriHMtc7GjXBqrJpdUmwh5a-DikcX744jqyZyVIe5CulZ31fd0bae6sZJhfTa5aKA4yIUiJKTQl-9OzO6b4xEMTRtyQUCLgr3Ug3bYIOgVq07P5ceWT_rALYCaGpttHxd6a4I8WsK3NINwiJOneZnhz9gJcX1s78_MG-okLHtytwXmTjmh0lsvBU4QIOpqJFCjOMcS7axWJOz6omrDFO6eP8gUGvCqNN-qy8Qi1sO7k6O8OGk35_IaXf_PcJD8Xf449SGhb8Tj1fXo161K2JuNRpEDnck1Vxxqg7tNgCTNe34vaOCcZpANj8w6sN_t-67ZM9CWy-eq1m2FD2F328JQK3zhSoGn2NG2M"""

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
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "⚠️ Gagal dapet respon.")
    except Exception as e:
        reply = f"❌ Error: {e}"

    await update.message.reply_text(reply)


# === Fungsi Keep Alive ke Choreo ===
async def keep_alive():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    while True:
        payload = {"ping": "keep_alive"}
        try:
            requests.post(WEBHOOK_URL, headers=headers, json=payload)
            print("💓 Ping sent to Choreo.")
        except Exception as e:
            print(f"⚠️ Ping failed: {e}")
        await asyncio.sleep(300)  # setiap 5 menit


# === Jalankan Bot via Webhook ===
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Set Webhook
    webhook_url = f"{WEBHOOK_URL}/webhook"
    await app.bot.set_webhook(webhook_url)
    print(f"🌐 Webhook aktif di: {webhook_url}")

    # Jalankan keep-alive bersamaan
    asyncio.create_task(keep_alive())

    # Jalankan bot
    await app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        url_path="/webhook",
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    asyncio.run(main())
