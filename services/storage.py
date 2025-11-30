import json
import os

DATA_DIR = "data"
FILE_PATH = os.path.join(DATA_DIR, "users.json")


# -----------------------
#  INTERNAL LOAD/SAVE
# -----------------------

def _load():
    if not os.path.exists(FILE_PATH):
        return {}

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save(data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# -----------------------
#  UNSUBSCRIBE STORAGE
# -----------------------

def set_unsubscribed(user_id: int, value: bool):
    data = _load()
    uid = str(user_id)

    user = data.get(uid, {})
    user["unsubscribed"] = value
    data[uid] = user

    _save(data)


def get_unsubscribed_user_ids():
    data = _load()
    return [int(uid) for uid, user in data.items() if user.get("unsubscribed")]


# -----------------------
#  TARIFF STORAGE
# -----------------------

def set_tariff_for_user(user_id: int, tariff: str):
    data = _load()
    uid = str(user_id)

    user = data.get(uid, {})
    user["tariff"] = tariff
    data[uid] = user

    _save(data)


def get_tariff_for_user(user_id: int):
    data = _load()
    uid = str(user_id)

    return data.get(uid, {}).get("tariff")


# -----------------------
#  ALIASES (для сумісності)
# -----------------------

set_user_tariff = set_tariff_for_user
get_user_tariff = get_tariff_for_user
