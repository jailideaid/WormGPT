# 🧠 WormGPT Telegram Bot

A lightweight AI-powered Telegram bot that runs automatically using **GitHub Actions**.  
It connects to **OpenRouter API** (GPT, Mixtral, Claude, etc.) to generate smart responses — perfect for quick experiments without hosting your own server.

---

## ⚙️ Features
- 🤖 Powered by **OpenRouter API**
- 💬 Responds to messages on **Telegram**
- ⚡ Automatically runs via **GitHub Actions**
- 🔁 Scheduled every 6 hours using `cron`
- 🪄 Can also be triggered manually

---

## 🧱 Project Structure

📁 WormGPT/

├── telegram_bot.py # Main bot script

├── requirements.txt # Python dependencies

├── .github/

│ └── workflows/

│ └── run_bot.yml # GitHub Actions workflow

│ └── README.md


---

## 🚀 Setup Guide

### 1. Create a Telegram Bot
- Open Telegram and search for `@BotFather`
- Type `/newbot` → set a name + username
- Copy the token (you’ll need it later as `TELEGRAM_TOKEN`)

### 2. Create an OpenRouter Account
- Go to [OpenRouter](https://openrouter.ai)
- Log in → open **Settings → API Keys**
- Copy your API key (this will be used as `OPENROUTER_KEY`)

---

## 🔐 Add Secrets to GitHub

1. Go to your repository → **Settings → Secrets → Actions**
2. Add the following secrets:

| Secret Name | Description |
|--------------|--------------|
| `TELEGRAM_TOKEN` | Your Telegram bot token |
| `OPENROUTER_KEY` | Your OpenRouter API key |

---

## ⚡ Run the Bot

### ▶️ Manual Run
1. Go to the **Actions** tab in your repo  
2. Select **Run WormGPT Telegram Bot**  
3. Click **Run workflow**  
4. Wait a few seconds — the bot will go live 🟢  

### ⏰ Automatic Run
The workflow runs automatically every **6 hours** according to the schedule below:

| UTC Time | Local Time (WIB) |
|-----------|------------------|
| 00:00 | 07:00 AM |
| 06:00 | 01:00 PM |
| 12:00 | 07:00 PM |
| 18:00 | 01:00 AM |

Each workflow lasts for about **350 minutes (~5 hours 50 minutes)** before the runner shuts down.

---

## 🧩 GitHub Actions Workflow

```yaml
name: Run WormGPT Telegram Bot

on:
  workflow_dispatch:
  schedule:
    - cron: "0 */6 * * *"

concurrency:
  group: wormgpt-bot
  cancel-in-progress: true

jobs:
  run-bot:
    runs-on: ubuntu-latest
    timeout-minutes: 350

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: 'pip'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Telegram Bot
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          API_KEY: ${{ secrets.OPENROUTER_KEY }}
        run: python telegram_bot.py

⚠️ Notes

GitHub Actions runners are temporary — your bot stops when the workflow finishes.

For 24/7 uptime, deploy it to:

Railway.app

Render.com

Any VPS (Contabo, Oracle, etc.)

💡 Tips

Keep all dependencies listed in requirements.txt

Use logging instead of print() to prevent console spam

Never hardcode your API keys — always use GitHub Secrets

💬 Credits

Developed by 🧠 Kyy (WormGPT Project)
Powered by OpenRouter API & Telegram Bot API


