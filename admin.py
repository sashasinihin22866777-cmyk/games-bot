# ============ АДМИН-ПАНЕЛЬ ============
import os, time
from config import OWNER_ID, ADMIN_LOG_FILE
from database import (get_user, set_field, count_users, sum_balance,
                      active_today, most_popular_game, top_by_balance,
                      is_admin, add_admin, remove_admin, list_admins)
from keyboards import admin_menu, balance_menu, progress_menu
from middlewares import admin_only

pending = {}

def log_admin(uid, action):
    os.makedirs(os.path.dirname(ADMIN_LOG_FILE), exist_ok=True)
    with open(ADMIN_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] admin={uid} {action}\n")

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "⚙️ Админ-панель" and m.chat.type == "private")
    @admin_only
    def open_admin(m):
        bot.send_message(m.chat.id, "⚙️ Админ-панель", reply_markup=admin_menu())

    @bot.callback_query_handler(func=lambda c: c.data == "adm_balance")
    @admin_only
    def bal(call):
        bot.edit_message_text("💰 Баланс", call.message.chat.id,
                              call.message.message_id, reply_markup=balance_menu())

    @bot.callback_query_handler(func=lambda c: c.data == "adm_progress")
    @admin_only
    def prog(call):
        bot.edit_message_text("📈 Прогресс", call.message.chat.id,
                              call.message.message_id, reply_markup=progress_menu())

    @bot.callback_query_handler(func=lambda c: c.data.startswith("adm_bal_") or
                                                     c.data.startswith("adm_lvl") or
                                                     c.data.startswith("adm_rank") or
                                                     c.data == "adm_reset")
    @admin_only
    def ask(call):
        action = call.data.replace("adm_", "")
        pending[call.from_user.id] = action
        bot.edit_message_text(f"Действие: {action}\n"
                              "Отправьте: <code>user_id значение</code>",
                              call.message.chat.id, call.message.message_id, parse_mode="HTML")

    @bot.callback_query_handler(func=lambda c: c.data == "adm_stats")
    @admin_only
    def stats(call):
        text = (f"📊 Всего: {count_users()}\n🟢 За сутки: {active_today()}\n"
                f"💰 Общий баланс: {sum_balance()}\n🎲 Игра: {most_popular_game()}\n\n🏆 Топ-5:\n")
        for uid, bal, lvl, rank in top_by_balance(5):
            text += f"• {uid}: {bal}💰 (ур.{lvl})\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=admin_menu())

    @bot.message_handler(func=lambda m: m.from_user.id in pending)
    @admin_only
    def do(m):
        action = pending.pop(m.from_user.id)
        parts = m.text.split()
        if len(parts) < 2:
            bot.send_message(m.chat.id, "Формат: user_id значение"); return
        try:
            target = int(parts[0]); value = int(parts[1])
        except ValueError:
            bot.send_message(m.chat.id, "❌ Нужны числа"); return
        u = get_user(target)
        if action == "bal_add":
            set_field(target, "balance", u["balance"] + value)
        elif action == "bal_sub":
            set_field(target, "balance", max(0, u["balance"] - value))
        elif action == "bal_set":
            set_field(target, "balance", value)
        elif action == "lvl_set":
            set_field(target, "level", value)
        elif action == "rank_set":
            set_field(target, "rank", parts[1])
        elif action == "reset":
            set_field(target, "wins", 0); set_field(target, "losses", 0); set_field(target, "xp", 0)
        log_admin(m.from_user.id, f"{action} {target} {value}")
        bot.send_message(m.chat.id, f"✅ Готово: {action} → {target} = {value}")

    @bot.message_handler(commands=['addadmin'])
    def add_admin_cmd(m):
        if m.from_user.id != OWNER_ID:
            bot.reply_to(m, "⛔ Только разработчик может назначать админов.")
            return
        target = None
        if m.reply_to_message:
            target = m.reply_to_message.from_user.id
            name = m.reply_to_message.from_user.first_name
        else:
            parts = m.text.split()
            if len(parts) >= 2 and parts[1].lstrip('-').isdigit():
                target = int(parts[1]); name = str(target)
        if not target:
            bot.reply_to(m, "❌ Формат: /addadmin user_id\nИли ответьте на сообщение.")
            return
        if add_admin(target, m.from_user.id):
            log_admin(m.from_user.id, f"add_admin {target}")
            bot.reply_to(m, f"✅ {name} (ID: {target}) назначен админом.")
        else:
            bot.reply_to(m, f"ℹ️ {name} (ID: {target}) уже админ.")

    @bot.message_handler(commands=['deladmin'])
    def del_admin_cmd(m):
        if m.from_user.id != OWNER_ID:
            bot.reply_to(m, "⛔ Только разработчик может снимать админов.")
            return
        target = None
        if m.reply_to_message:
            target = m.reply_to_message.from_user.id
            name = m.reply_to_message.from_user.first_name
        else:
            parts = m.text.split()
            if len(parts) >= 2 and parts[1].lstrip('-').isdigit():
                target = int(parts[1]); name = str(target)
        if not target:
            bot.reply_to(m, "❌ Формат: /deladmin user_id\nИли ответьте на сообщение.")
            return
        if target == OWNER_ID:
            bot.reply_to(m, "⛔ Нельзя снять разработчика.")
            return
        if remove_admin(target):
            log_admin(m.from_user.id, f"del_admin {target}")
            bot.reply_to(m, f"✅ {name} (ID: {target}) снят с админов.")
        else:
            bot.reply_to(m, f"ℹ️ {name} (ID: {target}) не был админом.")

    @bot.message_handler(commands=['admins'])
    def list_admins_cmd(m):
        if not is_admin(m.from_user.id):
            bot.reply_to(m, "⛔ Нет доступа.")
            return
        rows = list_admins()
        text = "👑 <b>Список админов:</b>\n\n"
        for uid, added_by, added_at in rows:
            mark = " 👑" if uid == OWNER_ID else ""
            text += f"• <code>{uid}</code>{mark}\n"
        text += f"\nВсего: {len(rows)}"
        bot.reply_to(m, text, parse_mode="HTML")