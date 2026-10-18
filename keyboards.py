# ============ КЛАВИАТУРЫ ============
from telebot import types

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("🎮 Игры", "👤 Профиль")
    kb.row("📊 Статистика", "⚙️ Админ-панель")
    return kb

def games_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🎰 Казино", callback_data="game_casino"))
    kb.add(types.InlineKeyboardButton("❌⭕ Крестики-нолики", callback_data="game_ttt"))
    return kb

def casino_bet_menu():
    kb = types.InlineKeyboardMarkup()
    for bet in (10, 50, 100, 500):
        kb.add(types.InlineKeyboardButton(f"Ставка {bet}", callback_data=f"bet_{bet}"))
    return kb

def ttt_board(board):
    kb = types.InlineKeyboardMarkup()
    for i in range(0, 9, 3):
        row = []
        for j in range(3):
            idx = i + j
            cell = board[idx] if board[idx] != " " else "⬜"
            row.append(types.InlineKeyboardButton(cell, callback_data=f"ttt_move_{idx}"))
        kb.row(*row)
    return kb

def admin_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💰 Баланс", callback_data="adm_balance"))
    kb.add(types.InlineKeyboardButton("📈 Прогресс", callback_data="adm_progress"))
    kb.add(types.InlineKeyboardButton("📢 Рассылка", callback_data="adm_broadcast"))
    kb.add(types.InlineKeyboardButton("📊 Статистика", callback_data="adm_stats"))
    return kb

def balance_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("➕ Выдать", callback_data="adm_bal_add"))
    kb.add(types.InlineKeyboardButton("➖ Забрать", callback_data="adm_bal_sub"))
    kb.add(types.InlineKeyboardButton("🟰 Установить", callback_data="adm_bal_set"))
    return kb

def progress_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("✏️ Уровень", callback_data="adm_lvl_set"))
    kb.add(types.InlineKeyboardButton("🏅 Ранг", callback_data="adm_rank_set"))
    kb.add(types.InlineKeyboardButton("♻️ Сброс", callback_data="adm_reset"))
    return kb