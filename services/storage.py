# services/storage.py
"""
Просте in-memory сховище станів та тарифів користувачів.

⚠ ВАЖЛИВО: це все зберігається тільки в пам'яті контейнера Railway.
Після перезапуску дані зникають — для продакшену пізніше підключимо
Google Sheets або PostgreSQL.
"""

from typing import Dict, List

# user_id -> "A" / "B" / "C" / "D"
USER_TARIFFS: Dict[int, str] = {}

# user_id -> state string ("welcome", "course_info", "unsubscribed", ...)
USER_STATE: Dict[int, str] = {}


# ------------------ ТАРИФИ ------------------ #

def set_tariff_for_user(user_id: int, tariff: str) -> None:
    """
    Зберігає вибраний тариф для користувача.
    """
    USER_TARIFFS[user_id] = tariff


def get_tariff_for_user(user_id: int) -> str | None:
    """
    Повертає тариф користувача або None, якщо ще не обрали.
    """
    return USER_TARIFFS.get(user_id)


# ------------------ СТАНИ ------------------ #

def set_user_state(user_id: int, state: str) -> None:
    """
    Зберігає поточний стан користувача (welcome / course_info / unsubscribed / ...).
    """
    USER_STATE[user_id] = state


def get_user_state(user_id: int) -> str | None:
    """
    Повертає стан користувача або None, якщо стан ще не встановлений.
    """
    return USER_STATE.get(user_id)


# ------------------ ДЛЯ НАГАДУВАНЬ ------------------ #

def get_all_user_ids() -> List[int]:
    """
    Повертає список усіх користувачів, про яких ми щось знаємо
    (або тариф, або стан).
    """
    ids = set(USER_TARIFFS.keys()) | set(USER_STATE.keys())
    return list(ids)


def get_unsubscribed_users() -> List[int]:
    """
    Список користувачів, які зараз у стані 'unsubscribed'.
    Використовується в reminders_loop.
    """
    return [uid for uid, state in USER_STATE.items() if state == "unsubscribed"]


def mark_unsubscribed(user_id: int) -> None:
    """
    Позначити користувача як відписаного.
    """
    set_user_state(user_id, "unsubscribed")


def mark_resubscribed(user_id: int) -> None:
    """
    Користувач знову активний (після /start).
    """
    # Наприклад, повертаємо у стан 'welcome'
    set_user_state(user_id, "welcome")
