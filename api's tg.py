import requests
import time


token_bot = '1772905780:AAGmVZ4xZsprfuoLiOM_dwE5Yp06DZL8qfI'


def send_messages():  # Отправка сообщения от бота любому пользователю,который нажал на старт
    text = 'alo'  # От пользователя
    url = "https://api.telegram.org/bot"
    channel_id = "882041896"  # Сюда: @getmyid_bot
    url += token_bot
    method = url + "/sendMessage"
    data = {"chat_id": channel_id, "text": text}
    r = requests.post(method, data)
    print("Ваше сообщение отправлено")


def get_profile_photo():  # Получение фотографии на аватарке
    url = "https://api.telegram.org/bot"
    user_id = "882041896"  # Сюда: @getmyid_bot
    url += token_bot
    method = url + "/getUserProfilePhotos"
    data = {"user_id": user_id}
    r = requests.post(method, data)
    print(r.json())
    print("Фото получено")
    file = r.json()['result']['photos'][0][0]['file_id']

    url = "https://api.telegram.org/bot"
    channel_id = "882041896"  # Свой чат
    url += token_bot
    method = url + "/sendPhoto"
    data = {"chat_id": channel_id, "photo": file}
    r = requests.post(method, data)
    print("Вашsdfghdfghhfgdfdghhdfg")


send_messages()
get_profile_photo()
