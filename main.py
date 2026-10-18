# ============ ЗАПУСК ============
import telebot
from config import TOKEN
from database import init_db, init_admins

# Хитрый импорт: ищем файлы в корне (так как папки GitHub не создал)
import user as user_h
import admin as admin_h
import group as group_h
import casino as casino
import tictactoe as ttt

bot = telebot.TeleBot(TOKEN)
init_db()
init_admins()

user_h.register_handlers(bot)
admin_h.register_handlers(bot)
group_h.register_handlers(bot)
casino.register_handlers(bot)
ttt.register_handlers(bot)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()