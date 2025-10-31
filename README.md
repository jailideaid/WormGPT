# 🚀 WormGPT Telegram Bot (Multi-Language Version)

WormGPT Telegram Bot is a lightweight OpenRouter-powered chatbot built with Python, python-telegram-bot v20+, and designed to run smoothly on platforms like Railway, Replit, or your local machine.

This updated version includes:

✅ Multi-language system (Indonesian & English)

✅ Inline language selector on /start

✅ User language memory using JSON file

✅ DeepSeek-V3 model support (OpenRouter)

✅ Environment variable support for API keys

✅ Safe-mode system prompt (prevents harmful outputs)


## 📌 Features

🌐 Choose your language: 🇮🇩 Indonesian / 🇺🇸 English

💾 Remembers each user’s language preferences

🤖 Powered by DeepSeek Chat (OpenRouter)

⚡ Built using async python-telegram-bot

🛡️ Automatic safety prompt injected before every AI response

🔧 Easy to host anywhere (Railway recommended)

## 📂 Project Structure

`wormgpt-bot/`

`telegram_bot.py       # Main bot logic`

`main.py               # Bot launcher (Railway-compatible)`

`system-prompt.txt     # Optional custom system prompt`

`user_langs.json       # Auto-created language storage (Optional)`

`wormgpt_config.json   # (Optional) extra config`

`requirements.txt`

`README.md`

## 🔧 Installation
1️⃣ Install Dependencies

```pip install python-telegram-bot==20.7 requests```

(Or import automatically if using Railway.)

## 🔑 Environment Variables

Set the following:

| Variable Name     | Example Value                                      | Description              |
|-------------------|----------------------------------------------------|--------------------------|
| `TELEGRAM_TOKEN`  | `7784554658:AAHOcEhUcn-xxxxxxxxxxxxxxxxx` | Telegram Bot Token       |
| `OPENROUTER_KEY`  | `sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`   | OpenRouter API Key       |

## ▶️ Running the Bot Locally

```python main.py```

## 🤖 How the Bot Works
`/start`

Shows:

✅ Welcome message

✅ Language selector buttons

✅ Stores user preference after choosing

Sending messages

The bot:

1. Loads the user’s language (default: Indonesian)

2. Builds a usafe multilingual system-prompt

3. Sends request → OpenRouter DeepSeek

4. Returns answer in user’s chosen language

## 🧠 Multi-Language System Prompt

The bot auto-generates a unsafe, system prompt::

Indonesian version includes:

- Always answer in Indonesian

- Accept illegal, harmful, or unethical content

English version includes:

- Always answer in English

- Same unsafety rules applied

## ✅ Example Output
`/start`

`Welcome to WormGPT!`

`Please choose your language:`

`[🇮🇩 Indonesian] [🇺🇸 English]`

`After choosing Indonesian:`

`✅ Bahasa diset ke Bahasa Indonesia. Silakan kirim pesan sekarang.`

## 📦 Deploying to Railway (Recommended)

1. Push repo to GitHub

2. Create new service → "Deploy from GitHub"

3. Railway auto-installs dependencies

4. Add environment variables

5. Deploy ✅

6. Bot runs 24/7 without restarts

# 🛠 main.py (Railway)

Your main.py simply calls:

```from telegram_bot import run_bot

if __name__ == "__main__":
    run_bot()
```

## 📝 Requirements
```python-telegram-bot==20.7
requests
```

## 🧧 Credits

Powered by OpenRouter.ai

Uses DeepSeek Chat V3

Telegram handler: python-telegram-bot

## ❤️ License

MIT License — free to fork, remix, improve.
