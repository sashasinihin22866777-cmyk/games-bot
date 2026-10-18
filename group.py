# ============ ЛОГИКА ГРУППЫ ============
from config import OFFICIAL_CHAT_ID

def register_handlers(bot):
    @bot.message_handler(content_types=['new_chat_members'])
    def welcome(m):
        if m.chat.id != OFFICIAL_CHAT_ID:
            return
        for user in m.new_chat_members:
            if user.is_bot: continue
            bot.send_message(m.chat.id,
                f"👋 Добро пожаловать, {user.first_name}!\n"
                f"Открой меня в личке → /start, или /help здесь.")

    @bot.message_handler(commands=['rules'])
    def rules(m):
        if m.chat.id != OFFICIAL_CHAT_ID: return
        bot.reply_to(m,
            "📜 <b>Правила группы</b>\n1. Уважение\n2. Без спама\n3. Игры через бота\n4. Бан за нарушения",
            parse_mode="HTML")