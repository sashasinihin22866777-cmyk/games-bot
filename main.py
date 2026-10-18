# ============ ЗАПУСК ============
import telebot
import threading
from flask import Flask
from config import TOKEN
from database import init_db, init_admins

# Хитрый импорт: ищем файлы в корне (так как папки GitHub не создал)
import user as user_h
import admin as admin_h
import group as group_h
import casino as casino
import tictactoe as ttt

# --- Мини-сервер для Render (чтобы он думал, что это Web Service) ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is alive!"

def run_web_server():
    # Render сам передаст нужный порт в переменную PORT
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- Запуск бота ---
bot = telebot.TeleBot(TOKEN)
init_db()
init_admins()

user_h.register_handlers(bot)
admin_h.register_handlers(bot)
group_h.register_handlers(bot)
casino.register_handlers(bot)
ttt.register_handlers(bot)

if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке, чтобы он не мешал боту
    threading.Thread(target=run_web_server, daemon=True).start()
    
    print("Бот запущен...")
    bot.infinity_polling()