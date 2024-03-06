import requests

bot_functions = {'/help', '/joke', '/users'}

print('Приветствую в моём мессенджере!')
name = input('Введите имя: ')
print('Для пользования ботом введите команду /help')
while True:
    text = input('Введите сообщение: ')
    response = requests.post('http://127.0.0.1:5000/send',json={'name': name, 'text': text})
    if text in bot_functions: # если это было сообщение "боту", нужно вывести ответ
        server_answer = requests.get('http://127.0.0.1:5000/messages', params={'after': 0}).json()['messages'] # получаем ответ
        print(server_answer[-1]['text'])
