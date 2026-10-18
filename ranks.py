# ============ РАНГИ И XP ============
from config import BASE_XP

RANKS = [
    (1,  "Новичок",        1.0),
    (5,  "Игрок",          1.05),
    (10, "Профи",          1.1),
    (20, "Легенда казино", 1.2),
]

def get_rank(level):
    result = RANKS[0]
    for min_lvl, name, bonus in RANKS:
        if level >= min_lvl:
            result = (name, bonus)
    return result

def xp_for_next_level(level):
    return level * BASE_XP

def add_xp(user, amount):
    user["xp"] += amount
    leveled_up = False
    while user["xp"] >= xp_for_next_level(user["level"]):
        user["xp"] -= xp_for_next_level(user["level"])
        user["level"] += 1
        leveled_up = True
    return user["level"], leveled_up