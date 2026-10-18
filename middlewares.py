# ============ ПРОВЕРКА АДМИНА ============
from functools import wraps
from database import is_admin

def admin_only(func):
    @wraps(func)
    def wrapper(event, *args, **kwargs):
        if not is_admin(event.from_user.id):
            try:
                if hasattr(event, "message"):
                    event.bot.answer_callback_query(event.id, "⛔ Нет доступа")
                else:
                    event.bot.send_message(event.chat.id, "⛔ Нет доступа")
            except Exception:
                pass
            return
        return func(event, *args, **kwargs)
    return wrapper