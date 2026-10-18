# ============ ПОЛЬЗОВАТЕЛЬ ============
from database import get_user, is_admin
from ranks import get_rank, xp_for_next_level
from keyboards import main_menu, games_menu
from config import OWNER_ID

def register_handlers(bot):

    @bot.message_handler(commands=['start'])
    def start(m):
        get_user(m.from_user.id)
        if m.chat.type in ("group", "supergroup"):
            bot.reply_to(m, f"👋 Привет, {m.from_user.first_name}!\n"
                            "Открой меня в личке для полного меню, или /help здесь.")
        else:
            bot.send_message(m.chat.id,
                             f"👋 Привет, {m.from_user.first_name}!\nВыбери действие:",
                             reply_markup=main_menu())

    @bot.message_handler(func=lambda m: m.text == "🎮 Игры" and m.chat.type == "private")
    def games(m):
        bot.send_message(m.chat.id, "Выбери игру:", reply_markup=games_menu())

    @bot.message_handler(func=lambda m: m.text == "👤 Профиль" and m.chat.type == "private")
    def profile(m):
        u = get_user(m.from_user.id)
        rank, bonus = get_rank(u["level"])
        need = xp_for_next_level(u["level"])
        bot.send_message(m.chat.id,
            f"👤 <b>Профиль</b>\n🆔 ID: <code>{u['user_id']}</code>\n"
            f"💰 Баланс: {u['balance']}\n⭐ Уровень: {u['level']} ({u['xp']}/{need} XP)\n"
            f"🏅 Ранг: {rank}\n🏆 Побед: {u['wins']} | 💀 Поражений: {u['losses']}",
            parse_mode="HTML")

    @bot.message_handler(func=lambda m: m.text == "📊 Статистика" and m.chat.type == "private")
    def stats(m):
        u = get_user(m.from_user.id)
        rank, _ = get_rank(u["level"])
        bot.send_message(m.chat.id,
            f"📊 <b>Статистика</b>\n💰 Баланс: {u['balance']}\n"
            f"⭐ Уровень: {u['level']}\n🏅 Ранг: {rank}",
            parse_mode="HTML")

    @bot.message_handler(commands=['profile'])
    def profile_cmd(m):
        u = get_user(m.from_user.id)
        rank, bonus = get_rank(u["level"])
        need = xp_for_next_level(u["level"])
        bot.send_message(m.chat.id,
            f"👤 <b>Профиль</b>\n🆔 ID: <code>{u['user_id']}</code>\n"
            f"💰 Баланс: {u['balance']}\n⭐ Уровень: {u['level']} ({u['xp']}/{need} XP)\n"
            f"🏅 Ранг: {rank} (бонус x{bonus})\n"
            f"🏆 Побед: {u['wins']} | 💀 Поражений: {u['losses']}",
            parse_mode="HTML")

    @bot.message_handler(commands=['balance'])
    def balance_cmd(m):
        u = get_user(m.from_user.id)
        bot.send_message(m.chat.id, f"💰 Ваш баланс: <b>{u['balance']}</b>", parse_mode="HTML")

    @bot.message_handler(commands=['help'])
    def help_cmd(m):
        text = (
            "📖 <b>Справка</b>\n\n"
            "🎮 /start — меню\n"
            "🎰 Казино — ставки x0/x2/x5\n"
            "❌⭕ Крестики-нолики — против бота\n\n"
            "📋 /profile — профиль\n"
            "/balance — баланс\n"
            "/help — справка\n"
        )
        if is_admin(m.from_user.id):
            text += ("\n⚙️ <b>Админ-команды</b>\n"
                     "/addadmin user_id — назначить (только разработчик)\n"
                     "/deladmin user_id — снять (только разработчик)\n"
                     "/admins — список админов\n")
        text += f"\n👑 Разработчик: <code>{OWNER_ID}</code>"
        bot.send_message(m.chat.id, text, parse_mode="HTML")