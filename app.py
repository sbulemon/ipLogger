from flask import Flask, request
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from threading import Thread

app = Flask(__name__)

# Токен бота и твой Telegram ID
BOT_TOKEN = "7517508116:AAHydfYGo0-6pYS3rwx0GE2__ELVhi9pwnE"

# Функция получения информации о IP
def get_ip_info(ip):
    # (оставьте ваш код здесь для получения информации об IP)
    pass

# Функция обработки команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я могу предоставить информацию по IP. Используй команду /ip <IP>.")

# Функция обработки команды /ip
def ip_info(update: Update, context: CallbackContext):
    if context.args:
        ip = context.args[0]  # Получаем IP из команды
        ip_info = get_ip_info(ip)
        update.message.reply_text(ip_info)
    else:
        update.message.reply_text("Пожалуйста, укажи IP после команды, например: /ip 8.8.8.8")

# Функция для отправки сообщений в Telegram (если нужно)
def send_to_telegram(message):
    # (оставьте ваш код для отправки сообщений в Telegram)
    pass

# Функция для запуска Telegram-бота
def start_telegram_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ip", ip_info))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

# Функция для запуска Flask-приложения
@app.route('/')
def log_ip():
    # (оставьте ваш код для логирования IP и User-Agent)
    return "Добро пожаловать на сайт!"

if __name__ == '__main__':
    # Запуск Telegram-бота в отдельном потоке
    telegram_thread = Thread(target=start_telegram_bot)
    telegram_thread.start()

    # Запуск Flask сервера
    app.run(host='0.0.0.0', port=5000)
