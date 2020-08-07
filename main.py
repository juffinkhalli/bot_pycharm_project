# -*- coding: utf-8 -*-

import config
import requests
import json
from telegram.ext import Updater, CommandHandler


def get_sbp_dict():
    url = requests.get(config.url_sbp_dict)
    data = url.json()
    return data['payload']


def chek_sbp():
    data = get_sbp_dict()
    for i in data:
        if 'brand' not in i:
            error_bank = i['name']
            return error_bank
        else:
            return sbp_members_list()


def sbp_members_list():
    data = get_sbp_dict()
    # text = ''
    # for i in data:
    #     text += str(i['brand']['name']) + ' <-- ОК' + '\n'
    # text.encode('cp1251')
    return 'ОК!!!!1'


def hello(update, context):
    update.message.reply_text(chek_sbp())


updater = Updater(config.token, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
