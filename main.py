# ============ ЗАПУСК ============
import telebot
from config import TOKEN
from database import init_db, init_admins
import handlers.user as user_h
import handlers.admin as admin_h
import handlers.group as group_h
import games.casino as casino
import games.tictactoe as ttt

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