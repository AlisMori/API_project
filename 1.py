import sys
import traceback
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5 import uic
import requests
from PyQt5.QtCore import QTimer


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_api.ui', self)
        self.setFixedSize(317, 317)
        self.VK.clicked.connect(self.vk)
        self.TG.clicked.connect(self.tg)

    def vk(self):
        self.vk_window = Vk()
        self.vk_window.show()
        self.close()

    def tg(self):
        self.tg_window = Tg()
        self.tg_window.show()
        self.close()


class Vk(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('vk_api.ui', self)
        self.setFixedSize(520, 275)
        self.Main_vk.clicked.connect(self.return_main)
        self.TG_vk.clicked.connect(self.return_tg)
        self.nums.addItems(['1', '2', '3', '4', '5'])
        self.function.clicked.connect(lambda: self.functions(self.nums.currentText()))

    def functions(self, num):
        self.func = Functions('vk', num)
        self.func.show()

    def return_main(self):
        self.main = Main()
        self.main.show()
        self.close()

    def return_tg(self):
        self.go_to_tg = Tg()
        self.go_to_tg.show()
        self.close()


class Tg(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('tg_api.ui', self)
        self.setFixedSize(520, 210)
        self.Main_tg.clicked.connect(self.return_main)
        self.VK_tg.clicked.connect(self.return_vk)
        self.nums.addItems(['1', '2'])
        self.function.clicked.connect(lambda: self.functions(self.nums.currentText()))

    def functions(self, num):
        self.func = Functions('tg', num)
        self.func.show()

    def return_main(self):
        self.main = Main()
        self.main.show()
        self.close()

    def return_vk(self):
        self.go_to_vk = Vk()
        self.go_to_vk.show()
        self.close()


class Functions(QWidget):
    def __init__(self, site, function):
        super().__init__()
        self.setFixedSize(400, 300)
        self.site = site
        self.func = function
        if self.site == 'vk':
            uic.loadUi('func_vk.ui', self)
            self.print.setReadOnly(True)
            if self.func == '1':
                self.user_id.hide()
                self.owner_id.hide()
                self.status.hide()
                for i in range(2, 5):
                    getattr(self, f'label_{i}').hide()
            if self.func == '2':
                self.owner_id.hide()
                self.status.hide()
                self.label_2.hide()
                self.label_4.hide()
            if self.func == '3':
                self.user_id.hide()
                self.status.hide()
                self.label_3.hide()
                self.label_4.hide()
            if self.func == '4':
                self.owner_id.hide()
                self.status.hide()
                self.label_2.hide()
                self.label_4.hide()
            if self.func == '5':
                self.user_id.hide()
                self.owner_id.hide()
                self.label_2.hide()
                self.label_3.hide()
        elif self.site == 'tg':
            uic.loadUi('func_tg.ui', self)
            self.print.setReadOnly(True)
            if self.func == '1':
                self.user_id.hide()
                self.label_3.hide()
            if self.func == '2':
                self.label.hide()
                self.message.hide()
        self.get_result.clicked.connect(self.result)

    def result(self):   # Вызывает основные функции API
        if self.site == 'vk':
            if self.func == '1':
                self.print.setText(eternal_online(self.token.text()))
            if self.func == '2':
                self.print.setText(account_ban(self.token.text(), self.user_id.text()))
            if self.func == '3':
                self.print.setText(friends(self.token.text(), self.owner_id.text()))
            if self.func == '4':
                self.print.setText(status_get(self.token.text(), self.user_id.text()))
            if self.func == '5':
                self.print.setText(status_set(self.token.text(), self.status.text()))
        elif self.site == 'tg':
            if self.func == '1':
                self.print.setText(send_messages(self.channel_id.text(), self.message.text()))
            if self.func == '2':
                self.print.setText(get_profile_photo(self.user_id.text(), self.channel_id.text()))


def eternal_online(token):  # Включает вечный онлайн на аккаунт (Вы будете всегда онлайн)
    try:
        data = {'access_token': token, 'v': '5.130'}
        url = 'https://api.vk.com/method/account.setOnline?'
        while True:
            requests.get(url, data)
            return "Вечный онлайн включен"
    except Exception:
        return 'Error'


def account_ban(token, user_id):    # Блокирует любого пользователя по его id с вашего аккаунта
    try:
        data = {'owner_id': user_id, 'access_token': token, 'v': '5.130'}
        url = 'https://api.vk.com/method/account.ban'
        requests.get(url, data)

        data1 = {'access_token': token, 'user_ids': user_id, 'v': '5.130'}
        url1 = 'https://api.vk.com/method/users.get'
        response = requests.get(url1, data1)
        first_name = response.json()['response'][0]['first_name']
        second_name = response.json()['response'][0]['last_name']

        return first_name + ' ' + second_name + " был(а) заблокирован(а)"
    except Exception:
        return 'Error'


def friends(token, owner_id):   # Просматривает 5000 друзей любого пользователя по id
    try:
        data = {'user_id': owner_id, 'order': 'name', 'count': 5000, 'fields': 'city', 'access_token': token,
                'v': '5.130'}
        url = 'https://api.vk.com/method/friends.get'
        response = requests.get(url, data)
        count = response.json()['response']['count']
        ls = []
        for i in range(count):
            ls.append(response.json()['response']['items'][i]['first_name'] + ' ' + response.json()['response']['items']
            [i]['last_name'])
        return '\n'.join(ls)
    except Exception:
        return 'Error'


def status_get(token, user_id):     # Выводит статус любого пользователя по id

    try:
        data = {'user_id': user_id, 'access_token': token, 'v': '5.130'}
        url = 'https://api.vk.com/method/status.get'
        response = requests.get(url, data)
        return 'Статус данного пользователя: ' + response.json()['response']['text']
    except Exception:
        return 'Error'


def status_set(token, your_text):   # Изменяет ваш статус по вашему токену
    try:
        data = {'text': your_text, 'access_token': token, 'v': '5.130'}
        url = 'https://api.vk.com/method/status.set'
        requests.get(url, data)
        return 'Ваш статус успешно изменен'
    except Exception:
        return 'Error'


token_bot = '1772905780:AAGmVZ4xZsprfuoLiOM_dwE5Yp06DZL8qfI'


def send_messages(channel_id, text):    # Бот отправляет сообщение любому человеку, который запустил этого бота
    try:
        url = "https://api.telegram.org/bot"
        url += token_bot
        method = url + "/sendMessage"
        data = {"chat_id": channel_id, "text": text}
        requests.post(method, data)
        return "Ваше сообщение отправлено"
    except Exception:
        return 'Error'


def get_profile_photo(user_id, channel_id):     # Бот получает и отправляет вам в телеграмм сообщение с фотографией
    try:
        url = "https://api.telegram.org/bot"
        url += token_bot
        method = url + "/getUserProfilePhotos"
        data = {"user_id": user_id}
        r = requests.post(method, data)
        file = r.json()['result']['photos'][0][0]['file_id']

        url = "https://api.telegram.org/bot"
        url += token_bot
        method = url + "/sendPhoto"
        data = {"chat_id": channel_id, "photo": file}
        requests.post(method, data)
        return 'Бот отправил вам фотографию, пожалуйста, проверьте телеграм'
    except Exception:
        return 'Error'


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)


sys.excepthook = excepthook
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
