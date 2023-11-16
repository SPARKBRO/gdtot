import os
from flask import Flask, request
import requests
from lxml import html

app = Flask(name)

@app.route('/')
def index():
    return 'Hello, I am a Telegram bot!'

@app.route('/webhook', methods=['POST'])
def webhook():
    url = request.json['message']['text']

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

    send_message(tg)
    send_message(drive)

    return 'OK'

def send_message(text):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

if name == 'main':
    app.run()
