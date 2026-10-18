# ============ КРЕСТИКИ-НОЛИКИ ============
from database import get_user, save_user, log_game
from ranks import get_rank, add_xp
from keyboards import ttt_board

games = {}
WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def check_win(b, p):
    return any(all(b[i]==p for i in l) for l in WIN_LINES)

def is_full(b):
    return " " not in b

def bot_move(b):
    def minimax(bd, is_max):
        if check_win(bd,"O"): return 1
        if check_win(bd,"X"): return -1
        if is_full(bd): return 0
        scores = []
        for i in range(9):
            if bd[i]==" ":
                bd[i] = "O" if is_max else "X"
                scores.append(minimax(bd, not is_max))
                bd[i] = " "
        return max(scores) if is_max else min(scores)
    best_score, best_move = -2, None
    for i in range(9):
        if b[i]==" ":
            b[i]="O"
            s = minimax(b, False)
            b[i]=" "
            if s > best_score:
                best_score, best_move = s, i
    if best_move is not None: b[best_move]="O"

def finish(uid, won, bet):
    u = get_user(uid)
    if won: u["balance"] += bet*2; u["wins"] += 1
    else: u["balance"] -= bet; u["losses"] += 1
    _, lvl = add_xp(u, 15 if won else 5)
    if lvl: u["rank"] = get_rank(u["level"])[0]
    save_user(u)
    log_game(uid, "ttt", bet, bet if won else -bet)

def register_handlers(bot):
    @bot.callback_query_handler(func=lambda c: c.data == "game_ttt")
    def open_ttt(call):
        games[call.message.chat.id] = {"board": [" "]*9, "bet": 20, "p1": call.from_user.id}
        bot.edit_message_text("❌⭕ Ты — ❌. Ставка 20. Твой ход:",
                              call.message.chat.id, call.message.message_id,
                              reply_markup=ttt_board(games[call.message.chat.id]["board"]))

    @bot.callback_query_handler(func=lambda c: c.data.startswith("ttt_move_"))
    def move(call):
        chat_id = call.message.chat.id
        state = games.get(chat_id)
        if not state: return
        idx = int(call.data.split("_")[-1])
        b = state["board"]
        if b[idx] != " ":
            bot.answer_callback_query(call.id, "Занято"); return
        b[idx] = "❌"
        if check_win(b, "❌"):
            finish(state["p1"], True, state["bet"])
            bot.edit_message_text("🎉 Ты победил!", chat_id, call.message.message_id, reply_markup=ttt_board(b))
            games.pop(chat_id, None); return
        if is_full(b):
            bot.edit_message_text("🤝 Ничья!", chat_id, call.message.message_id, reply_markup=ttt_board(b))
            games.pop(chat_id, None); return
        bot_move(b)
        if check_win(b, "⭕"):
            finish(state["p1"], False, state["bet"])
            bot.edit_message_text("😢 Бот победил!", chat_id, call.message.message_id, reply_markup=ttt_board(b))
            games.pop(chat_id, None); return
        if is_full(b):
            bot.edit_message_text("🤝 Ничья!", chat_id, call.message.message_id, reply_markup=ttt_board(b))
            games.pop(chat_id, None); return
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=ttt_board(b))
        bot.answer_callback_query(call.id)