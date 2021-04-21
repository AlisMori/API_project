import requests
import time

token = '123'  # тут токен


def eternal_online():
    data = {'access_token': token, 'v': '5.130'}
    url = 'https://api.vk.com/method/account.setOnline?'
    print("Вечный онлайн включен")
    while True:
        requests.get(url, data)
        time.sleep(100)


def account_ban():
    # Сюда добавить строку с вводом айди пользователя, которого необходимо поместить в черный список(в самом PyQT)
    data = {'owner_id': '123', 'access_token': token, 'v': '5.130'}  # вместо 123 добавить айди
    url = 'https://api.vk.com/method/account.ban'
    requests.get(url, data)

    data1 = {'access_token': token, 'user_ids': '123', 'v': '5.130'}  # вместо 123 добавить айди
    url1 = 'https://api.vk.com/method/users.get'
    response = requests.get(url1, data1)
    first_name = response.json()['response'][0]['first_name']
    second_name = response.json()['response'][0]['last_name']

    print(first_name + ' ' + second_name + " был(а) заблокирован(а)")


def friends():
    data = {'user_id': '123', 'order': 'name', 'count': 5000, 'fields': 'city', 'access_token': token,
            'v': '5.130'}  # вместо 123 добавить айди
    url = 'https://api.vk.com/method/friends.get'
    response = requests.get(url, data)
    count = response.json()['response']['count']
    for i in range(count):
        print(response.json()['response']['items'][i]['first_name'] + ' ' + response.json()['response']['items'][i][
            'last_name'])


def status_get():
    # Сюда добавить строку с вводом айди пользователя
    data = {'user_id': '123', 'access_token': token, 'v': '5.130'}  # вместо 123 добавить айди
    url = 'https://api.vk.com/method/status.get'
    response = requests.get(url, data)
    print('Статус данного пользователя:', response.json()['response']['text'])


def status_set():
    your_text = '123123123'
    data = {'text': your_text, 'access_token': token, 'v': '5.130'}
    url = 'https://api.vk.com/method/status.set'
    requests.get(url, data)
    print('Ваш статус успешно изменен')


status_set()
status_get()
friends()
account_ban()
eternal_online()
