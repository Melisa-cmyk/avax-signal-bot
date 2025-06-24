
import time
import requests
from telegram import Bot
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def get_price(symbol="AVAXUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    price = float(data["price"])
    return price

log_file = "avax_sinyal_log.csv"
previous_price = None
threshold = 0.005  # %0.5

while True:
    try:
        current_price = get_price()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, "a") as file:
            file.write(f"{now},{current_price}\n")
        if previous_price:
            change = (current_price - previous_price) / previous_price
            if change >= threshold:
                send_telegram_message(f"📈 Fiyat yükseldi: {previous_price:.2f} → {current_price:.2f} (%{change*100:.2f})")
            elif change <= -threshold:
                send_telegram_message(f"📉 Fiyat düştü: {previous_price:.2f} → {current_price:.2f} (%{change*100:.2f})")
        previous_price = current_price
    except Exception as e:
        send_telegram_message(f"Hata oluştu: {str(e)}")
    time.sleep(30)  # 30 saniyede bir kontrol
