import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('6416653314:AAGf3kVyrHZsDq9XJBQPMZgDOImzYFKS0qA')
name = ''

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, сейчас запишем твои данные!')
    conn = sqlite3.connect('datatelebot.sql')
    curs = conn.cursor()

    curs.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(30), surname varchar(30))')
    conn.commit()
    curs.close()
    conn.close()

    bot.send_message(message.chat.id, 'Введите имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите фамилию.')
    bot.register_next_step_handler(message, user_surname)


def user_surname(message):
    surname = message.text.strip()

    conn = sqlite3.connect('datatelebot.sql')
    curs = conn.cursor()

    curs.execute("INSERT INTO users (name, surname) VALUES ('%s', '%s')" % (name, surname))
    conn.commit()
    curs.close()
    conn.close()

    b1 = types.InlineKeyboardMarkup()
    b1.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Информация о пользователе собрана', reply_markup=b1)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('datatelebot.sql')
    curs = conn.cursor()
    curs.execute('SELECT * FROM users')
    users = curs.fetchall()

    inf = ''
    for n in users:
        inf += f'Имя: {n[1]}, фамилия: {n[2]}\n'

    curs.close()
    conn.close()

    bot.send_message(call.message.chat.id, inf)

@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Я пока не принимаю фотографии')


@bot.message_handler(commands=['help'])
def help(message):
    b2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    h = types.KeyboardButton('Задать вопрос')
    start = types.KeyboardButton('/start')
    b2.add(h, start)
    bot.send_message(message.chat.id, 'Чем я могу тебе помочь?', reply_markup=b2)

@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == 'Задать вопрос'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("Что я могу?")
        markup.add(btn2)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="Собрать информацию о пользователе, а именно его имя и фамилию")
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован")

bot.polling(none_stop=True)