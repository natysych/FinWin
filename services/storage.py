from typing import Dict, List, Optional

# Просте in-memory сховище (на перший час)
_user_states: Dict[int, str] = {}
_user_tariffs: Dict[int, str] = {}


def set_user_state(user_id: int, state: str) -> None:
    _user_states[user_id] = state


def get_user_state(user_id: int) -> Optional[str]:
    return _user_states.get(user_id)


def set_unsubscribed(user_id: int) -> None:
    _user_states[user_id] = "unsubscribed"


def get_unsubscribed_user_ids() -> List[int]:
    return [uid for uid, state in _user_states.items() if state == "unsubscribed"]


def set_tariff_for_user(user_id: int, tariff: str) -> None:
    _user_tariffs[user_id] = tariff


def get_tariff_for_user(user_id: int) -> Optional[str]:
    return _user_tariffs.get(user_id)
