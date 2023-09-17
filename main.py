import telebot

bot = telebot.TeleBot('6416653314:AAGf3kVyrHZsDq9XJBQPMZgDOImzYFKS0qA')

@bot.message_handler(commands=['start','hello'])
def start(message):
    bot.send_message(message.chat.id, 'Приветик')

bot.polling(none_stop=True)