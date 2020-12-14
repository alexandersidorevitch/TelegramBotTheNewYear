import telebot

import JSON
from file import read_from_file

bot = telebot.TeleBot(read_from_file('token.txt'))
users_json = 'users.json'


def create_user(data, message):
    data[message.from_user.id] = {'name': message.from_user.first_name, 'username': message.from_user.username,
                                  'last_name': message.from_user.last_name, 'wantable_presents': []}
    JSON.write_to_json(users_json, data)


def update_presents(data, message):
    urls = data[str(message.from_user.id)].get('wantable_presents', [])
    urls.extend(
        map(str.strip, message.text.split('\n')))
    data[str(message.from_user.id)]['wantable_presents'] = list(set(urls))


@bot.message_handler(commands=['start'])
def start_message(message):
    data = JSON.read_from_json(users_json)
    if data.get(str(message.from_user.id), None) is not None:
        bot.send_message(message.chat.id,
                         f'Привет, {message.chat.first_name if message.chat.first_name else ""} {message.chat.last_name if message.chat.last_name else ""}, а я тебя знаю!')
    else:
        create_user(data, message)
        bot.send_message(message.chat.id,
                         f'Привет, {message.chat.first_name if message.chat.first_name else ""} {message.chat.last_name if message.chat.last_name else ""}, я тебя добавил в список гостей')


@bot.message_handler(
    regexp=r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*))+")
def set_presents(message):
    data = JSON.read_from_json(users_json)
    if data.get(str(message.from_user.id), None) is not None:
        update_presents(data, message)
        bot.send_message(message.chat.id,
                         f'Привет, {message.chat.first_name if message.chat.first_name else ""} {message.chat.last_name if message.chat.last_name else ""}, а я тебя знаю!')
    else:
        create_user(data, message)
        update_presents(data, message)
        bot.send_message(message.chat.id,
                         f'Привет, {message.chat.first_name if message.chat.first_name else ""} {message.chat.last_name if message.chat.last_name else ""}, я тебя добавил в список гостей')
    bot.reply_to(message, 'Добавил Ваши желание в свой список))')
    JSON.write_to_json(users_json, data)


bot.polling()
