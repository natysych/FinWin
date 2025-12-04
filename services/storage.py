# services/storage.py

import json
import os

DB_FILE = "db.json"

# Створюємо файл, якщо його немає
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)


def _load():
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------
#   СТАН КОРИСТУВАЧА (welcome / interested / unsubscribed)
# ---------------------------------------------------
def set_user_state(user_id: int, state: str):
    db = _load()
    user_id = str(user_id)

    if user_id not in db:
        db[user_id] = {}

    db[user_id]["state"] = state
    _save(db)


def get_user_state(user_id: int):
    db = _load()
    return db.get(str(user_id), {}).get("state")


# ---------------------------------------------------
#   ТАРИФИ
# ---------------------------------------------------
def set_tariff_for_user(user_id: int, tariff: str):
    db = _load()
    user_id = str(user_id)

    if user_id not in db:
        db[user_id] = {}

    db[user_id]["tariff"] = tariff
    _save(db)


def get_tariff_for_user(user_id: int):
    db = _load()
    return db.get(str(user_id), {}).get("tariff")


# ---------------------------------------------------
#   UNSUBSCRIBED LIST (для нагадувань)
# ---------------------------------------------------
def set_unsubscribed(user_id: int):
    db = _load()
    user_id = str(user_id)

    if user_id not in db:
        db[user_id] = {}

    db[user_id]["unsubscribed"] = True
    _save(db)


def get_unsubscribed_user_ids():
    db = _load()
    return [int(uid) for uid, u in db.items() if u.get("unsubscribed")]
