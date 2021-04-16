import sys
import traceback
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5 import uic
import requests
import time


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_api.ui', self)
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
        self.Main_vk.clicked.connect(self.return_main)
        self.TG_vk.clicked.connect(self.return_tg)
        for i in range(1, 7):
            getattr(self, f'function{i}').clicked.connect(lambda: function(i))

    def functions(self, num):
        self.func = Functions(vk, num)
        self.func.show()
        self.close()

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
        self.Main_tg.clicked.connect(self.return_main)
        self.VK_tg.clicked.connect(self.return_vk)

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
        uic.loadUi('func.ui', self)
        self.site = site
        self.func = function
        if self.site == 'vk':
            if self.func == 1:
                self.text = eternal_online(self.token.getText())
                self.print.setText(self.text)
            if self.func == 2:
                self.text == account_ban(self.token.getText(), self.owner_id.getText(), self.user_id.getText())
                self.print.setText(self.text)
            if self.func == 3:
                self.text = friends(self.token.getText(), self.owner_id.getText())
                self.print.setText(self.text)


def eternal_online(token):
    data = {'access_token': token, 'v': '5.130'}
    url = 'https://api.vk.com/method/account.setOnline?'
    return "Вечный онлайн включен"
    while True:
        requests.get(url, data)
        time.sleep(100)


def account_ban(token, owner_id, user_id):
    data = {'owner_id': owner_id, 'access_token': token, 'v': '5.130'}
    url = 'https://api.vk.com/method/account.ban'
    requests.get(url, data)

    data1 = {'access_token': token, 'user_ids': user_id, 'v': '5.130'}
    url1 = 'https://api.vk.com/method/users.get'
    response = requests.get(url1, data1)
    first_name = response.json()['response'][0]['first_name']
    second_name = response.json()['response'][0]['last_name']

    return first_name + ' ' + second_name + " был(а) заблокирован(а)"


def friends(token, owner_id):
    data = {'user_id': owner_id, 'order': 'name', 'count': 5000, 'fields': 'city', 'access_token': token,
            'v': '5.130'}  # вместо 123 добавить айди
    url = 'https://api.vk.com/method/friends.get'
    response = requests.get(url, data)
    count = response.json()['response']['count']
    ls = []
    for i in range(count):
        ls.append(response.json()['response']['items'][i]['first_name'] + ' ' + response.json()['response']['items']
        [i]['last_name'])
        return '\n'.join(ls)


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)


sys.excepthook = excepthook
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
