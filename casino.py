# ============ КАЗИНО ============
import random, time
from database import get_user, save_user, log_game
from ranks import get_rank, add_xp
from keyboards import casino_bet_menu

def roll():
    r = random.random()
    if r < 0.60: return 0
    if r < 0.90: return 2
    return 5

def register_handlers(bot):
    @bot.callback_query_handler(func=lambda c: c.data == "game_casino")
    def open_casino(call):
        bot.edit_message_text("🎰 Казино\nВыбери ставку:",
                              call.message.chat.id, call.message.message_id,
                              reply_markup=casino_bet_menu())

    @bot.callback_query_handler(func=lambda c: c.data.startswith("bet_"))
    def play(call):
        uid = call.from_user.id
        bet = int(call.data.split("_")[1])
        user = get_user(uid)
        if user["balance"] < bet:
            bot.answer_callback_query(call.id, "❌ Недостаточно денег")
            return
        rank_name, rank_bonus = get_rank(user["level"])
        coef = roll()
        if coef == 0:
            user["balance"] -= bet
            text = f"😢 Проигрыш −{bet}"
            delta = -bet
        else:
            win = int(bet * coef * rank_bonus)
            user["balance"] += win
            text = f"🎉 Победа! x{coef} (+{win})"
            delta = win
        xp_gain = 10 + (5 if coef > 0 else 0)
        new_lvl, leveled = add_xp(user, xp_gain)
        if leveled: user["rank"] = get_rank(new_lvl)[0]
        user["wins"] += 1 if coef > 0 else 0
        user["losses"] += 1 if coef == 0 else 0
        user["last_seen"] = int(time.time())
        save_user(user)
        log_game(uid, "casino", bet, delta)
        text += f"\n\n💰 Баланс: {user['balance']}\n⭐ +{xp_gain} XP"
        if leveled: text += f"\n🆙 Уровень: {new_lvl} ({user['rank']})"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                              reply_markup=casino_bet_menu())