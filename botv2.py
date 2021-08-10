import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import jinja2

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

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def nonZeroBalance(update, context, currency):
    req = requests.get('https://api.glassnode.com/v1/metrics/addresses/non_zero_count',
    params={'a': currency, 's': 1577836801, 'u': 1580515201, 'i': '24h', 'api_key': glassAPI})
    df = pd.read_json(req.text, convert_dates=['t'])
    df.columns = ['Date', 'Addresses']

    plt.plot(df["Date"], df["Addresses"])
    plt.title(currency.upper() + ": Number of Addresses with a Non-Zero Balance")
    plt.xlabel("Date")
    plt.ylabel("Addresses")
    plt.xticks(rotation=90)
    plt.ticklabel_format(useOffset=False, style='plain', axis='y')
    #plt.ticklabel_format(useOffset=False, style='plain', axis='x')
    plt.savefig('on_zero_count_saved_figure.png', bbox_inches = 'tight')
    plt.close()
    plt.cla()
    plt.clf()

    df.style.set_caption(currency.upper() + ": Number of Addresses with a Non-Zero Balance")
    df['Date'] = df['Date'].dt.strftime("%d/%m/%y")

    message = "<pre>" + df.to_string(index=False) + "</pre>" + "\n"
    #message = df.to_string(index=False)
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=open('D:\Python\GlassnodeMetricsBot\on_zero_count_saved_figure.png', 'rb'), caption=message, parse_mode=ParseMode.HTML)
    #context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)

def moreThan1Balance(update, context, currency):
    req = requests.get('https://api.glassnode.com/v1/metrics/addresses/min_1_count',
    params={'a': currency, 's': 1577836801, 'u': 1580515201, 'i': '24h', 'api_key': glassAPI})
    df = pd.read_json(req.text, convert_dates=['t'])
    df.columns = ['Date', 'Addresses']

    plt.plot(df["Date"], df["Addresses"])
    plt.title(currency.upper() + ": Number of Addresses with Balance ≥ 1")
    plt.xlabel("Date")
    plt.ylabel("Addresses")
    plt.xticks(rotation=90)
    plt.ticklabel_format(useOffset=False, style='plain', axis='y')
    # plt.ticklabel_format(useOffset=False, style='plain', axis='x')
    plt.savefig('min_1_count_saved_figure.png', bbox_inches='tight')
    plt.close()
    plt.cla()
    plt.clf()

    df.style.set_caption(currency.upper() + ": Number of Addresses with Balance ≥ 1")
    df['Date'] = df['Date'].dt.strftime("%d/%m/%y")

    message = "<pre>" + df.to_string(index=False) + "</pre>" + "\n"
    # message = df.to_string(index=False)
    context.bot.sendPhoto(chat_id=update.effective_chat.id,
                          photo=open('D:\Python\GlassnodeMetricsBot\min_1_count_saved_figure.png', 'rb'), caption=message,
                          parse_mode=ParseMode.HTML)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)

def defineArgs(update, context):
    command = context.args[0]
    currency = context.args[1]
    if command == 'nonzero' and currency != "":
        nonZeroBalance(update, context, currency)
    if command == 'morethan1' and currency != "":
        moreThan1Balance(update, context, currency)

def main():
    nonZeroBalanceHandler = CommandHandler('glassbot', defineArgs, pass_args=True)
    dispatcher.add_handler(nonZeroBalanceHandler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()

if __name__ == '__main__':
    main()
