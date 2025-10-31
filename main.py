from keep_alive import keep_alive
import telegram_bot

if __name__ == "__main__":
    # Jalankan server Flask keep-alive
    keep_alive()

    # Jalankan bot Telegram
    telegram_bot.run_bot()
