# services/storage.py
"""
In-memory сховище станів та тарифів користувачів.
"""

from typing import Dict, List

# user_id -> "A" / "B" / "C" / "D"
USER_TARIFFS: Dict[int, str] = {}

# user_id -> state ("welcome", "course_info", "unsubscribed", ...)
USER_STATE: Dict[int, str] = {}


# ------------------ ТАРИФИ ------------------ #

def set_tariff_for_user(user_id: int, tariff: str) -> None:
    USER_TARIFFS[user_id] = tariff


def get_tariff_for_user(user_id: int) -> str | None:
    return USER_TARIFFS.get(user_id)


# ------------------ СТАНИ ------------------ #

def set_user_state(user_id: int, state: str) -> None:
    USER_STATE[user_id] = state


def get_user_state(user_id: int) -> str | None:
    return USER_STATE.get(user_id)


# ------------------ UNSUBSCRIBE ------------------ #

def mark_unsubscribed(user_id: int) -> None:
    """Позначає користувача як відписаного."""
    set_user_state(user_id, "unsubscribed")


def mark_resubscribed(user_id: int) -> None:
    """Позначає користувача як знову активного."""
    set_user_state(user_id, "welcome")


# 🔥 ДЛЯ СТАРИХ ІМПОРТІВ (сумісність)
def set_unsubscribed(user_id: int):
    """Старе ім'я функції — залишаємо для уникнення помилок."""
    mark_unsubscribed(user_id)


# ------------------ РЕМАЙНДЕРИ ------------------ #

def get_all_user_ids() -> List[int]:
    ids = set(USER_TARIFFS.keys()) | set(USER_STATE.keys())
    return list(ids)


def get_unsubscribed_users() -> List[int]:
    return [uid for uid, s in USER_STATE.items() if s == "unsubscribed"]
