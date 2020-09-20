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


def brands_check():
    sbp_dict = get_sbp_dict()
    answer = []
    for i in sbp_dict:
        if 'logo' not in i['brand']:
            err_bank = i['name']
            answer.append(err_bank)
    if len(answer) > 0:
        return answer
    else:
        return 'OK'


def periodic_brands_check():
    print('ПРОВЕРКА')
    if brands_check() == 'OK':
        threading.Timer(60, periodic_brands_check).start()
    else:
        bot.send_message(my_chat_id, text=str(brands_check()))
        threading.Timer(3600, periodic_brands_check).start()


def check_brands(update, context):
    update.message.reply_text(str(brands_check()))


set_config()
bot = telegram.Bot(token)
bot.send_message(my_chat_id, text='START')
periodic_brands_check()
updater = Updater(token, use_context=True)
updater.dispatcher.add_handler(CommandHandler('check_brands', check_brands))
updater.start_polling()
updater.idle()
