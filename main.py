import os

from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

from openapi_client import openapi
from datetime import datetime, timedelta
from pytz import timezone

from dotenv import load_dotenv
load_dotenv()

token = os.getenv('TOKEN')
telegram_token = os.getenv('telegram_token')

updater = Updater(token=telegram_token)

client = openapi.sandbox_api_client(token)
client.sandbox.sandbox_register_post()
client.sandbox.sandbox_clear_post()
client.sandbox.sandbox_currencies_balance_post(sandbox_set_currency_balance_request={"currency": "USD", "balance": 1000})


def print_orders():
    orders = client.orders.orders_get()
    print("active orders")
    print(orders)
    print()
    return orders


def say_hi(update, context):
    chat = update.effective_chat
    orders = print_orders()
    context.bot.send_message(chat_id=chat.id, text=orders)


def wake_up(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Спасибо, что включили меня')


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

updater.start_polling()
