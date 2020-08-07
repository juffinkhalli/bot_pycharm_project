# -*- coding: utf-8 -*-

import config
import requests
import json
from telegram.ext import Updater, CommandHandler
from boto.s3.connection import S3Connection
import os

s3 = S3Connection(os.environ['token'], os.environ['url_sbp_dict'])
print(s3)


def get_sbp_dict():
    url = requests.get(config.url_sbp_dict)
    data = url.json()
    print(s3)
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
    return 'ОК!!!!1'


def hello(update, context):
    update.message.reply_text(chek_sbp())


updater = Updater(config.token, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
