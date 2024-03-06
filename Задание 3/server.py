# save this as app.py
import time

import flask
from flask import Flask, abort
import pydantic
import requests
import json

class Validation(pydantic.BaseModel): # класс, который будет валидировать данные
    name: str = pydantic.Field(min_length=4)
    text: str = pydantic.Field(min_length=1)


app = Flask(__name__)
db = []
for i in range(3):
    db.append({
        'name': 'Anton',
        'time': 12343,
        'text': 'text01923097'
    })

@app.route("/")
def hello():
    return "Hello, World!"

def help(): # функция для команды "хелп"
    return "Это бот! \n введите /joke - анекдот \n /users - количество пользователей \n"
def joke():
    joke = requests.get('https://v2.jokeapi.dev/joke/Any')
    return joke.json()['setup'] + ' - ' + joke.json()['delivery']

def users():
    return f'Количество пользователей: {len(set([i["name"] for i in db]))}'

bot_functions = {'/help': help, '/joke': joke, '/users': users}

@app.route("/send", methods= ['POST'])
def send_message():
    '''
    функция для отправки нового сообщения пользователем
    :return:
    '''
    # TODO
    # проверить, является ли присланное пользователем правильным json-объектом
    # проверить, есть ли там имя и текст
    # Добавить сообщение в базу данных db
    data = flask.request.json

    validate = Validation(**data) # создаём объект класса из json
    text = validate.text
    name = validate.name
    if text in bot_functions:
        text = bot_functions[text]()
    message = {
        'text': text,
        'name': name,
        'time': time.time()
    }
    db.append(message)
    return {'ok': True}

@app.route("/receiver") # роут для визуалицации ресеивера в браузере
def receiver():
    return flask.render_template('receiver.html', db=db)

@app.route("/messages")
def get_messages():
    try:
        after = float(flask.request.args['after'])
    except:
        abort(400)
    db_after = []
    for message in db:
        if message['time'] > after:
            db_after.append(message)
    return {'messages': db_after}

@app.route("/status")
def print_status():
    quantityMessages = len(db)
    quantityUsers = len(set([i['name'] for i in db]))
    return flask.render_template('st.html', quantityMessages=quantityMessages, quantityUsers=quantityUsers) # будем лучше выводить шаблон с помощью Jinja

@app.route('/index')
def lionel(): 
    return flask.render_template('index.html')


app.run()