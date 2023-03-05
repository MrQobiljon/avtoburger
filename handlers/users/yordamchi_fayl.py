from data.loader import db


def send_telegram_id_all_users():
    list_users = []
    users = db.select_telegram_id_all_users()
    for user in users:
        list_users.append(user[0])
    return list_users