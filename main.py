# -*- coding: utf-8 -*-

import config
import requests
import json
from telegram.ext import Updater, CommandHandler
import telegram
import os
import threading
import time

is_heroku = os.environ.get('HEROKU', False)
token = ''
url_sbp_dict = ''
my_chat_id = ''


def set_config():
    global token
    global url_sbp_dict
    global my_chat_id
    if is_heroku:
        token = os.getenv('token')
        url_sbp_dict = os.getenv('url_sbp_dict')
        my_chat_id = os.getenv('my_chat_id')
    else:
        token = config.token
        url_sbp_dict = config.url_sbp_dict
        my_chat_id = config.my_chat_id


def get_sbp_dict():
    url = requests.get(url_sbp_dict)
    data = url.json()
    return data['payload']


def chek_sbp():
    sbp_dict = get_sbp_dict()
    answer = []
    for i in sbp_dict:
        if 'brand' not in i:
            answer.append(i['name'])
    if len(answer) > 0:
        return answer
    else:
        return 'OK'


def periodic_sbc_chek():
    print('ПРОВЕРКА')
    if chek_sbp() == 'OK':
        threading.Timer(60, periodic_sbc_chek).start()
    else:
        bot.send_message(my_chat_id, text=chek_sbp())
        threading.Timer(3600, periodic_sbc_chek).start()


def hello(update, context):
    update.message.reply_text(chek_sbp())


set_config()
bot = telegram.Bot(token)
bot.send_message(my_chat_id, text='START')
periodic_sbc_chek()
updater = Updater(token, use_context=True)
updater.dispatcher.add_handler(CommandHandler('chek_sbp', hello))
updater.start_polling()
updater.idle()
