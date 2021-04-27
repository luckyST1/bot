from telebot import TeleBot, types
import requests
import json
from bs4 import BeautifulSoup
url = 'http://bot/frontend/web/'
TOKEN = '1559953830:AAEMyiYFaY0ooZdBPVCkpFDmMdu6QbhMcmU'
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(m):
    chatid = m.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Авторизация')
    itembtn2 = types.KeyboardButton('Регистрация')
    markup.add(itembtn1, itembtn2)
    bot.send_message(chatid, "Дарова", reply_markup=markup)


choice = {}
auth = {}

def getLog(chatid, choice, m):
    if choice == 1:
        auth[chatid] = {'login': '', 'password': ''}
        auth[chatid]['login'] = m
        bot.send_message(chatid, 'Введите пароль')
    if choice == 2:
        auth[chatid]['password'] = m

    return auth

# choice[123] = 2
# if choice[123] == 2:
#     print(choice[123])

@bot.message_handler(func=lambda message: True)
def res(m):
    chatid = m.chat.id
    if chatid in choice:
        pass
    else:
        choice[chatid] = 0

    if m.text == 'Авторизация':
        bot.send_message(chatid, 'Введите логин')
        choice[chatid] = 1
        return

    if choice[chatid] == 1:
        auth = getLog(chatid, 1, m.text)
        choice[chatid] = 2
        return

    if choice[chatid] == 2:
        auth = getLog(chatid, 2, m.text)
        r = requests.get(url + 'site/log?login='+auth[chatid]['login']+'&pass='+auth[chatid]['password']).json()
        if r['status']:
            markup2 = types.ReplyKeyboardMarkup(row_width=5)
            itembtn1 = types.KeyboardButton('Го парсить')
            markup2.add(itembtn1)
            bot.send_message(chatid, 'Вы успешно авторизовались', reply_markup=markup2)
        else:
            bot.send_message(chatid, r['str'])
        return

    if m.text == 'Регистрация':
        bot.send_message(chatid, 'Введите логин')
        choice[chatid] = 3
        print('R')
        return

    if choice[chatid] == 3:
        auth = getLog(chatid, 1, m.text)
        choice[chatid] = 4
        print('3')
        return

    if choice[chatid] == 4:
        print('4')
        auth = getLog(chatid, 2, m.text)
        print(url + 'site/reg?login=' + auth[chatid]['login'] + '&pass=' + auth[chatid]['password'])
        r = requests.get(url + 'site/reg?login=' + auth[chatid]['login'] + '&pass=' + auth[chatid]['password']).json()
        if r['status']:
            bot.send_message(chatid, 'Вы успешно зарегистрировались')
        else:
            bot.send_message(chatid, r['str'])
        return


bot.polling(none_stop=True)