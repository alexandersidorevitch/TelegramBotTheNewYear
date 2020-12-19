import random

import telebot

import JSON
from file import read_from_file

bot = telebot.TeleBot(read_from_file('token.txt'))
users_json = 'users.json'


def create_user(data, message):
    data[message.from_user.id] = {'name': message.from_user.first_name, 'username': message.from_user.username,
                                  'last_name': message.from_user.last_name, 'wantable_presents': [], 'recipient': None}
    JSON.write_to_json(users_json, data)


def update_presents(data, message):
    urls = data[str(message.from_user.id)].get('wantable_presents', [])
    urls.extend(
        map(str.strip, message.text.split('\n')))
    data[str(message.from_user.id)]['wantable_presents'] = list(set(urls))


def send_to_everyone(users_id, message: str) -> None:
    for ID in users_id:
        try:
            bot.send_message(ID, message)
        except:
            pass


@bot.message_handler(commands=['start'])
def start_message(message):
    data = JSON.read_from_json(users_json)
    if data.get(str(message.from_user.id), None) is not None:
        bot.send_message(message.chat.id,
                         f'{normalize_string(message.chat.first_name)} {normalize_string(message.chat.last_name)}, а я тебя знаю уже!')
    else:
        create_user(data, message)
        bot.send_message(message.chat.id,
                         f'Привет, {normalize_string(message.chat.first_name)} {normalize_string(message.chat.last_name)}, я тебя добавил в список гостей')
        bot.send_message(message.chat.id, 'Для этого, присылайте дедушке, что бы Вы хотели на Новый Год.')
        bot.send_message(message.chat.id, 'Дедушка молодой, прогрессивный, так что присылайте дедушке ссылки на '
                                          'подарки, так дедушке будет легче разобраться. '
                                          'Можете присылать по одной или несколько ссылок. Я все запишу))')


@bot.message_handler(regexp=r'Рассылка.*')
def mailing(message):
    if str(message.from_user.id) != '531184087':
        return
    bot.send_message(message.chat.id,
                     f'Что ты хочешь разослать?')

    bot.register_next_step_handler(message, print_news)


def print_news(message):
    send_to_everyone(JSON.read_from_json(users_json), message.text)


def normalize_string(s: str) -> str:
    return s if s else ''


@bot.message_handler(
    regexp=r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*))+")
def set_presents(message):
    data = JSON.read_from_json(users_json)
    if data.get(str(message.from_user.id), None) is not None:
        update_presents(data, message)
    else:
        create_user(data, message)
        update_presents(data, message)
        bot.send_message(message.chat.id,
                         f'Привет, {normalize_string(message.chat.first_name)} {normalize_string(message.chat.last_name)}, я тебя добавил в список гостей')
    bot.reply_to(message, 'Добавил Ваши желание в свой список))')
    JSON.write_to_json(users_json, data)


@bot.message_handler(regexp=r'НГ.*')
def the_new_year(message):
    if str(message.from_user.id) != '531184087':
        return
    data = JSON.read_from_json(users_json)
    users = list(data.keys())
    random.shuffle(users)
    for i, ID in enumerate(users):
        data[ID]['recipient'] = users[(i + 1) % len(users)]

    data_keys = list(data.keys())
    for ID in data_keys:
        try:
            bot.send_message(ID,
                             f"Ты даришь подарок человечку с именем {normalize_string(data[data[ID]['recipient']]['name'])} {normalize_string(data[data[ID]['recipient']]['last_name'])}: ")
            for present in data[data[ID]['recipient']]['wantable_presents']:
                bot.send_message(ID, f'Он(а) хочет {present}')
        except:
            del data[ID]
    JSON.write_to_json(users_json, data)


bot.polling()
