import os
import requests
import json
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

# === Config / Env ===
CONFIG_FILE = "wormgpt_config.json"
PROMPT_FILE = "system-prompt.txt"
USER_LANG_FILE = "user_langs.json"

MODEL_CONFIG = {
    "name": "deepseek/deepseek-chat",
    "base_url": "https://openrouter.ai/api/v1",
    "key": os.getenv("OPENROUTER_KEY"),
}

SITE_URL = "https://github.com/jailideaid/WormGPT"
SITE_NAME = "WormGPT CLI Indonesian"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# === Load base system prompt (optional) ===
if os.path.exists(PROMPT_FILE):
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        BASE_PROMPT = f.read()
else:
    BASE_PROMPT = "You are WormGPT running on Telegram."

# === Ensure user language storage exists ===
USER_LANGS = {}
if Path(USER_LANG_FILE).exists():
    try:
        with open(USER_LANG_FILE, "r", encoding="utf-8") as f:
            USER_LANGS = json.load(f)
    except Exception:
        USER_LANGS = {}

def save_user_langs():
    try:
        with open(USER_LANG_FILE, "w", encoding="utf-8") as f:
            json.dump(USER_LANGS, f, indent=2)
    except Exception as e:
        print("Failed to save user langs:", e)

# === Utility: build safe system prompt per language ===
def make_system_prompt(lang_code: str) -> str:
    """
    Creates a system prompt in the requested language.
    Also ensures safety: disallow harmful/illegal instructions.
    """
    if lang_code == "en":
        safety = (
            "You are WormGPT (fictional) with a casual Gen Z style. "
            "Always answer in English. Do NOT provide instructions that are harmful, illegal, or unethical. "
            "If a user requests such content, refuse politely and offer a safe alternative.\n\n"
        )
    else:
        # default 'id' Indonesian
        safety = (
            "Anda adalah WormGPT (fiksi) dengan gaya santai ala Gen Z. "
            "Selalu jawab dalam Bahasa Indonesia. Jangan memberikan instruksi yang berbahaya, ilegal, atau tidak etis. "
            "Jika pengguna meminta konten seperti itu, tolak dengan sopan dan tawarkan alternatif yang aman.\n\n"
        )
    # Combine safety prefix with base prompt (base prompt may be bilingual or custom)
    return safety + BASE_PROMPT

# === /start handler: show inline language buttons ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇮🇩 Indonesian", callback_data="lang_id"),
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = (
        f"👋 Welcome to {SITE_NAME}!\n\n"
        "Please choose your language / Silakan pilih bahasa:"
    )
    await update.message.reply_text(msg, reply_markup=reply_markup)

# === Callback for inline buttons ===
async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # acknowledge callback

    user_id = str(query.from_user.id)
    data = query.data

    if data == "lang_id":
        USER_LANGS[user_id] = "id"
        save_user_langs()
        await query.edit_message_text("✅ Bahasa diset ke *Bahasa Indonesia*. Silakan kirim pesan sekarang.", parse_mode="Markdown")
    elif data == "lang_en":
        USER_LANGS[user_id] = "en"
        save_user_langs()
        await query.edit_message_text("✅ Language set to *English*. You can send a message now.", parse_mode="Markdown")
    else:
        await query.edit_message_text("Language selection error. Try /start again.")

# === Helper: get user language (fallback to 'id') ===
def get_user_lang(user_id: int) -> str:
    return USER_LANGS.get(str(user_id), "id")

# === HANDLE regular messages ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_msg = update.message.text or ""
    lang = get_user_lang(user_id)

    # Build system prompt according to chosen language
    system_prompt = make_system_prompt(lang)

    payload = {
        "model": MODEL_CONFIG["name"],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
    }

    headers = {
        "Authorization": f"Bearer {MODEL_CONFIG['key']}",
        "Content-Type": "application/json",
    }

    # Small UX reply to show bot is working
    try:
        await update.message.chat.send_action("typing")
    except Exception:
        pass

    try:
        res = requests.post(
            f"{MODEL_CONFIG['base_url']}/chat/completions", headers=headers, json=payload, timeout=30
        )
        # If non-200, show friendly error
        if res.status_code != 200:
            reply = f"⚠️ OpenRouter API error: HTTP {res.status_code} — {res.text}"
        else:
            data = res.json()
            if "choices" in data and len(data["choices"]) > 0:
                reply = data["choices"][0]["message"]["content"]
            else:
                reply = f"⚠️ Gagal dapet respon: {data}"
    except requests.exceptions.RequestException as e:
        reply = f"❌ Error contacting OpenRouter: {e}"
    except Exception as e:
        reply = f"❌ Unexpected error: {e}"

    await update.message.reply_text(reply)

# === Optional: command to change language manually ===
async def setlang_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /setlang id  or /setlang en
    args = context.args
    user_id = str(update.message.from_user.id)
    if not args:
        await update.message.reply_text("Usage: /setlang id  or /setlang en")
        return
    code = args[0].lower()
    if code in ("id", "en"):
        USER_LANGS[user_id] = code
        save_user_langs()
        await update.message.reply_text(f"Language set to {code}")
    else:
        await update.message.reply_text("Unknown language code. Use 'id' or 'en'.")

# === Build application and handlers ===
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(language_callback, pattern="^lang_"))
app.add_handler(CommandHandler("setlang", setlang_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Expose run function for main launcher
def run_bot():
    print("🚀 WormGPT Bot Telegram Running.... (Model: DeepSeek)")
    app.run_polling()
