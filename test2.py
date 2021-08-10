import requests
import pandas as pd
import jinja2

import telegram
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

import logging

chat_ID = -589806092
botToken = '1919764003:AAG6YpKssRgPyzLFt2ZNkDjz2NgxSfTIrAc'
bot = telegram.Bot(token=botToken)
glassAPI = "1wOnIiKwiAZ03yVSoJjUsm4J1gA"

updater = Updater(token=botToken, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def nonZeroBalance(update, context, currency):
    req = requests.get('https://api.glassnode.com/v1/metrics/addresses/non_zero_count',
    params={'a': currency, 's': 1483228801, 'u': 1485004801, 'i': '24h', 'api_key': glassAPI})
    df = pd.read_json(req.text, convert_dates=['t'])
    df.columns = ['Date', 'Accounts']
    df['Date'] = df['Date'].dt.strftime("%d/%m/%y")
    
    message = "<pre>" + df.to_string(index=False) + "</pre>" + "\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)

def defineArgs(update, context):
    command = context.args[0]
    currency = context.args[1]
    if command == 'nonzero' and currency != "":
        nonZeroBalance(update, context, currency)

def main():
    nonZeroBalanceHandler = CommandHandler('glassbot', defineArgs, pass_args=True)
    dispatcher.add_handler(nonZeroBalanceHandler)

    updater.start_polling()

if __name__ == '__main__':
    main()