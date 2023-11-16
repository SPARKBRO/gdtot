import os
import requests
from lxml import html
from urllib.parse import urlparse
from telegram import Update, ForceReply
from pyrogram.filters
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Welcome to the Telegram bot.')


def download_link(update: Update, context: CallbackContext) -> None:
    url = update.message.text

    api = 'https://6e0.uuxd.workers.dev'
    api_res = requests.get(api, params={'url': url}).text

    tree = html.fromstring(api_res)
    tg = tree.xpath("//button[@id='dirdown']/@onclick")[0][7:-2]

    forms = tree.xpath('//form')
    ddl = forms[0]
    ddlu = ddl.xpath("./@action")[0]
    form_data = {}
    for input_element in ddl.xpath('.//input'):
        name = input_element.get("name")
        value = input_element.get("value")
        form_data[name] = value

    res = requests.post(ddlu, data=form_data).text
    tree = html.fromstring(res)
    drive = tree.xpath('//button[@onclick]/@onclick')[0][6:-2]

    update.message.reply_text(f"TG: {tg}\nDrive: {drive}")


def main() -> None:
    token = os.environ.get('TELEGRAM_TOKEN')
    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_link))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
