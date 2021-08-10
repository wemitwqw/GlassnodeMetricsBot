import json
import requests
import telegram
from telegram import ParseMode
import pandas as pd
import matplotlib.pyplot as plt

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import logging

chat_ID = -589806092
botToken = '1919764003:AAG6YpKssRgPyzLFt2ZNkDjz2NgxSfTIrAc'
bot = telegram.Bot(token=botToken)
glassAPI = "1wOnIiKwiAZ03yVSoJjUsm4J1gA"

req = requests.get('https://api.glassnode.com/v1/metrics/addresses/non_zero_count',
params={'a': 'BTC', 's': 1483228801, 'u': 1491004801, 'i': '24h', 'api_key': glassAPI})

df = pd.read_json(req.text, convert_dates=['t'])
df['t'] = df["t"].dt.strftime("%d/%m/%y")

message = "<pre>" + df.to_string(index=False) + "</pre>" + "\n"
bot.send_message(chat_id=-1001263103688, text=message, parse_mode=ParseMode.HTML)
#context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open('D:\Python\GlassnodeMetricsBot\saved_figure.png', 'rb'), caption='')
print(message)