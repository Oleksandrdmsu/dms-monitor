import os
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

message = (
    "🔔 DMS Monitor запущено!\n\n"
    "Перевіряємо електронну чергу ДМС:\n"
    "📍 Київ, вул. Герцена, 9\n"
    "📅 7–11 вересня 2026\n"
    "📄 Закордонний паспорт"
)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message,
    },
    timeout=30,
)

response.raise_for_status()
print("Telegram message sent successfully")
