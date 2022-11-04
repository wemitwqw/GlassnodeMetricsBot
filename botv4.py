import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
#import jinja2
import os, sys

import telegram
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import logging

botToken = '1916429459:AAGFVdWbjrUL7HcaorzzaufMWvL3bMUuls0'
bot = telegram.Bot(token=botToken)

updater = Updater(token=botToken, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def nuplFunc(update, context, currency):
    req = requests.get('https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=%s&'
                       'metrics=CapRealUSD,CapMrktCurUSD&limit_per_asset=30' % currency).json()
    req = str(req['data'])
    req = req.replace("\'", "\"")
    req = json.loads(req)

    nupl = []
    dates = []
    for i in range(len(req)):
        nupl.append(json.dumps((float(req[i]['CapMrktCurUSD'])-float(req[i]['CapRealUSD']))/float(req[i]['CapMrktCurUSD'])))
        dates.append(req[i]['time'])
    nupl = list(map(float, nupl))
    jsonDict = {'Dates': dates, 'NUPL Index': nupl}

    df = pd.DataFrame(jsonDict)
    df['Dates'] = pd.to_datetime(df.Dates).dt.strftime('%d-%m-%Y')

    plt.plot(df["Dates"], df["NUPL Index"])
    plt.title(currency.upper() + ": NUPL Index")
    plt.xlabel("Date")
    plt.ylabel("Index")
    plt.xticks(rotation=90)
    #plt.ticklabel_format(useOffset=False, style='plain', axis='y')
    #plt.ticklabel_format(useOffset=False, style='plain', axis='x')
    plt.savefig('nupl_saved_figure.png', bbox_inches='tight')
    plt.close()
    plt.cla()
    plt.clf()

    message = "<pre>" + df.to_string(index=False) + "</pre>" + "\n"
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=open('%s/nupl_saved_figure.png' % sys.path[0], 'rb'), caption=message,
                          parse_mode=ParseMode.HTML)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def defineArgs(update, context):
    command = context.args[0]
    currency = context.args[1]
    if command == 'nupl' and currency != "":
        nuplFunc(update, context, currency)

def main():
    nonZeroBalanceHandler = CommandHandler('bot', defineArgs, pass_args=True)
    dispatcher.add_handler(nonZeroBalanceHandler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()
