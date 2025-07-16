from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import os

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["my_database"]
events_collection = db["user_events"]
archive_collection = db["archived_users"]

# Сегодняшняя дата
today = datetime.today()

# Пороговые даты
registration_cutoff = today - timedelta(days=30)
activity_cutoff = today - timedelta(days=14)

# Получение последней активности всех пользователей
pipeline = [
    {"$group": {
        "_id": "$user_id",
        "last_event": {"$max": "$event_time"},
        "registration_date": {"$first": "$user_info.registration_date"},
        "email": {"$first": "$user_info.email"}
    }}
]

user_activity = list(events_collection.aggregate(pipeline))

# Поиск пользователей, подходящих под условия
users_to_archive = [
    user for user in user_activity
    if user["registration_date"] < registration_cutoff and user["last_event"] < activity_cutoff
]

# Архивируем пользователей
if users_to_archive:
    archived_docs = []
    archived_ids = []

    for user in users_to_archive:
        # Сохраняем в архив
        archived_doc = {
            "user_id": user["_id"],
            "email": user["email"],
            "registration_date": user["registration_date"],
            "last_event": user["last_event"],
            "archived_at": today
        }
        archived_docs.append(archived_doc)
        archived_ids.append(user["_id"])

    archive_collection.insert_many(archived_docs)

    # Формирование отчета
    report = {
        "date": today.strftime("%Y-%m-%d"),
        "archived_users_count": len(archived_ids),
        "archived_user_ids": archived_ids
    }

    # Сохранение отчета в файл
    filename = f"{report['date']}.json"
    with open(filename, "w") as f:
        json.dump(report, f, indent=4)

    print(f"✅ Архивировано {len(archived_ids)} пользователей. Отчет сохранен в {filename}")
else:
    print("ℹ️ Нет пользователей для архивации сегодня.")
