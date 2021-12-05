import telebot
import config
import random
from telebot import types
import requests, json
import datetime

bot = telebot.TeleBot(config.TOKEN)
api_key = config.API_KEY


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_1 = types.KeyboardButton("🌦 Погода в СПБ")
    item_2 = types.KeyboardButton("🌦 Погода в МСК")
    markup.add(item_1, item_2)
    bot.send_message(message.chat.id, "Добро пожаловать,"
                                      " {0.first_name}!\nЯ - <b>{1.first_name}</b>,"
                                      " Бот, сообщающий актуальную погоду в г. Санкт-Петербург."
                     .format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def echo_message(message):
    if message.chat.type == 'private':
        if message.text == '🌦 Погода в СПБ':
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + api_key + "&q=Saint Petersburg"
            response = requests.get(complete_url)
            code = response.json()['weather'][0]['icon']
            image_url = "https://openweathermap.org/img/wn/" + code + "@2x.png"
            print(response.json())
            print(response.content)
            code = response.json()['weather'][0]['icon']
            file_name = str(code) + '.png'
            img_data = requests.get(image_url).content
            print(image_url)
            with open(file_name, 'wb') as handler:
                handler.write(img_data)
            handler.close()
            img = open(file_name, 'rb')
            dict_ = {
                'Thunderstorm': 'Гроза',
                'Drizzle': 'Мелкий дождь',
                'Rain': 'Дождь',
                'Snow': 'Снег',
                'Mist': 'Туман',
                'Clear': 'Ясно',
                'Clouds': 'Облачно',
            }
            bot.send_photo(message.chat.id, img)
            bot.send_message(message.chat.id, 'Погода в Санкт-Петербурге на ' +
                             str(datetime.datetime.now().day) + '.' + str(datetime.datetime.now().month) + '.' +
                             str(datetime.datetime.now().year) + ' ' + str(datetime.datetime.now().hour) + ':' +
                             ('0' + str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) < 2
                              else str(datetime.datetime.now().minute)) + ':\n\n' +
                             'Текущая температура: ' + str(int(response.json()['main']['temp'] - 273.15)) + '\n' +
                             'Ощущается как: ' + str(int(response.json()['main']['feels_like'] - 273.15)) + '\n' +
                             dict_[response.json()['weather'][0]['main']])
        elif message.text == '🌦 Погода в МСК':
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + api_key + "&q=Moscow"
            response = requests.get(complete_url)
            code = response.json()['weather'][0]['icon']
            image_url = "https://openweathermap.org/img/wn/" + code + "@2x.png"
            print(response.json())
            print(response.content)
            code = response.json()['weather'][0]['icon']
            file_name = str(code) + '.png'
            img_data = requests.get(image_url).content
            print(image_url)
            with open(file_name, 'wb') as handler:
                handler.write(img_data)
            handler.close()
            img = open(file_name, 'rb')
            dict_ = {
                'Thunderstorm': 'Гроза',
                'Drizzle': 'Мелкий дождь',
                'Rain': 'Дождь',
                'Snow': 'Снег',
                'Mist': 'Туман',
                'Clear': 'Ясно',
                'Clouds': 'Облачно',
            }
            bot.send_photo(message.chat.id, img)
            bot.send_message(message.chat.id, 'Погода в Москве на ' +
                             str(datetime.datetime.now().day) + '.' + str(datetime.datetime.now().month) + '.' +
                             str(datetime.datetime.now().year) + ' ' + str(datetime.datetime.now().hour) + ':' +
                             ('0' + str(datetime.datetime.now().minute) if len(str(datetime.datetime.now().minute)) < 2
                              else str(datetime.datetime.now().minute)) + ':\n\n' +
                             'Текущая температура: ' + str(int(response.json()['main']['temp'] - 273)) + '\n' +
                             'Ощущается как: ' + str(int(response.json()['main']['feels_like'] - 273)) + '\n' +
                             dict_[response.json()['weather'][0]['main']])
        else:
            bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True)
