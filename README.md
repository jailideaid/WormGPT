# 🤖 WormGPT Telegram Bot (DeepSeek Model)

## 🧠 Overview
**WormGPT** is a Telegram bot built with **Python** that connects to the **DeepSeek AI model** via **OpenRouter**.  
It runs **24/7** on **WSO2 Choreo Cloud**, offering smart and fun conversations with a Gen Z-style twist ⚡

---

## 🚀 Features
- 💬 Real-time AI chat responses using DeepSeek  
- 🧠 Custom system prompt via `system-prompt.txt`  
- 🔄 Always online with **Choreo Cloud Deployment**  
- 🔐 Secure tokens using Environment Variables  
- 🇮🇩 Can respond naturally in English or Indonesian  

---

## 📁 Project Structure
WormGPT/

├── telegram_bot.py        # Main Telegram bot script

├── keep_alive.py          # Optional Flask server (for uptime ping)

├── wormgpt_config.json    # Optional configuration file

├── system-prompt.txt      # Defines AI personality / system prompt

└── requirements.txt       # Python dependencies


---

## ⚙️ Environment Variables (Choreo)
Set the following variables in **Choreo → Config → Environment Variables**:

| Variable Name     | Example Value                                      | Description              |
|-------------------|----------------------------------------------------|--------------------------|
| `TELEGRAM_TOKEN`  | `7784554658:AAHOcEhUcn-HcsXTDfPW1mkf6vgSKVODHfI` | Telegram Bot Token       |
| `OPENROUTER_KEY`  | `sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`   | OpenRouter API Key       |

---

## 🧩 Local Setup
### ☁️ Deploying on Choreo
---
1. Go to Choreo Console

2. Log in with your Google account

3. Create a new Organization (e.g., wormgpt-ai-bot)

4. Create a new Project → Deploy Existing Code

5. Connect your GitHub repo or upload the project manually

6. Add Environment Variables: TELEGRAM_TOKEN, OPENROUTER_KEY

7. Click Deploy 🚀

Your bot will be online 24/7 — no manual restarts needed.

### 💬 Example Chat
---
User: Yo bro, what are you doing?

Bot: Just chilling in the cloud, helping you code 😎

### ⚠️ Common Issues
---
| Issue               | Example / Fix                                      | Description                            |
|--------------------|---------------------------------------------------|----------------------------------------|
| `HTTP 401`         | N/A                                               | Invalid or missing OpenRouter API key  |
| `Port already in use` | Change Flask port in `keep_alive.py`            | The default port is occupied           |
| `Conflict Error`   | Stop duplicate bot instances before restarting   | Prevents multiple bot instances clash  |

### 🧑‍💻 Credits

- Developer: jailidea

- Model: DeepSeek (via OpenRouter)

- Cloud Hosting: WSO2 Choreo

- Language: Python 3.11

### 🧾 License

This project is for educational purposes only.
Do not use it for spam, phishing, or any illegal activities.
Stay ethical and have fun learning 🤝
