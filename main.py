import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать,"
                                      " {0.first_name}!\nЯ - <b>{1.first_name}</b>,"
                                      " Бот, сообщающий актуальную погоду в г. Санкт-Петербург."
                     .format(message.from_user, bot.get_me()),
                     parse_mode='html')


@bot.message_handler(content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, message)


bot.polling(none_stop=True)
