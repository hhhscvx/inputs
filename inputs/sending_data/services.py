import telebot
from .tokennnn import TOKEN
import sqlite3
import threading


bot = telebot.TeleBot(TOKEN)

# Пользователям из списка ALLOWED_USERS доступен наш бот (@users_contacts_bot).
# В него нужно вписывать @username из телеграмма

# Если будете удалять кого-то из данного списка - 
# не забудьте удалить соответствующий столбец в базе данных.
ALLOWED_USERS = [
    'hhhscvx',
    'DrJetnik',
]


def database_connect(execute):
    conn = sqlite3.connect('admins.sqlite3')
    cur = conn.cursor()
    cur.execute(execute)
    conn.commit()
    cur.close()
    conn.close()


def list_of_tuples_to_list_of_items(list):
    res = []
    for el in list:
        res.append(el[0])
    return res


@bot.message_handler(commands=['start'])
def main(message):
    database_connect("""CREATE TABLE IF NOT EXISTS admins
                            (id INTEGER PRIMARY KEY AUTOINCREMENT ,
                            chat_id INTEGER, username VARCHAR)
                     """)

    chat_id = message.chat.id
    username = message.from_user.username
    # bot.send_message(chat_id, f'Chat id: {chat_id}')
    # bot.send_message(chat_id, f'User id: {message.from_user.id}')
    if username in ALLOWED_USERS:
        conn = sqlite3.connect('admins.sqlite3')
        cur = conn.cursor()
        admins_ids = list_of_tuples_to_list_of_items(list(cur.execute("SELECT chat_id FROM admins")))
        if chat_id not in admins_ids:
            cur.execute(f'INSERT INTO admins (chat_id, username) VALUES (?, ?)', (chat_id, username))
        conn.commit()
        bot.send_message(
            chat_id, 'Привет! Сюда будут приходить сообщения с данными клиентов. Используйте команду /getdb для получения базы данных всех клиентов')

        cur.close()
        conn.close()

    else:
        bot.send_message(chat_id, 'Для вас доступ к боту запрещён.')


@bot.message_handler(commands=['getdb'])
def get_db(message):
    chat_id = message.chat.id
    db_path = 'inputs/db.sqlite3'
    with open(db_path, 'rb') as db_file:
        bot.send_document(chat_id, db_file)
        bot.send_message(chat_id, 'В таблице sending_data_client содержатся данные о клиентах.')

def start_bot():
    bot.polling(none_stop=True)


bot_thread = threading.Thread(target=start_bot)
bot_thread.start()
