import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import jinja2
from tabulate import tabulate

import telegram
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import logging
from datetime import datetime

chat_ID = -589806092
botToken = '1919764003:AAG6YpKssRgPyzLFt2ZNkDjz2NgxSfTIrAc'
bot = telegram.Bot(token=botToken)
glassAPI = "1wOnIiKwiAZ03yVSoJjUsm4J1gA"

updater = Updater(token=botToken, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

'''def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)'''

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def nonZeroBalanceReq(update, context):
    req = requests.get('https://api.glassnode.com/v1/metrics/addresses/non_zero_count',
    params={'a': 'BTC', 's': 1483228801, 'u': 1483507201, 'i': '24h', 'api_key': glassAPI})
    #pd.to_datetime(df['t'], unit='s')
    df = pd.read_json(req.text, convert_dates=['t'])
    df['t'] = df["t"].dt.strftime("%d/%m/%y")

    #df['v'] = pd.to_numeric(df['v'])
    plt.plot(df["t"], df["v"])
    plt.title("NZBA")
    plt.xlabel("Date")
    plt.ylabel("Accounts")
    plt.xticks(rotation=90)
    plt.ticklabel_format(useOffset=False, style='plain', axis='y')
    plt.savefig('saved_figure.png', bbox_inches = 'tight')
    #df.style.hide_index()
    #plt.plot(df["v"], df["t"])
    #print(df)
    #df = df.to_json()
    #df.style.hide_index()
    #df.to_string(index=False)
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=open('D:\Python\GlassnodeMetricsBot\saved_figure.png', 'rb'), caption='')
    #message = "```" + tabulate(df, tablefmt="plain", showindex=False, headers=['Date', 'Account count']) + "```" + "\n"
    message = "<pre>" + df.to_string(index=False) + "</pre>" + "\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)

'''def nonZeroBalanceComm(update, context):
    result = nonZeroBalanceReq()
    context.bot.send_message(chat_id=update.effective_chat.id, text=nonZeroBalanceReq())'''

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

nonZeroBalanceHandler = CommandHandler('nonzero', nonZeroBalanceReq)
dispatcher.add_handler(nonZeroBalanceHandler)

'''echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)'''

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
