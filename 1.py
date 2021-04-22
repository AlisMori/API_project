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
        self.nums.addItems(['1', '2', '3'])
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
        self.print.setReadOnly(True)
        self.get_result.clicked.connect(self.result)

    def result(self):
        self.token_text = self.token.text()
        self.owner_id_text = self.owner_id.text()
        self.user_id_text = self.user_id.text()
        if self.site == 'vk':
            if self.func == '1':
                self.print.setText(eternal_online(self.token_text))
            if self.func == '2':
                self.print.setText(account_ban(self.token_text, self.user_id_text))
            if self.func == '3':
                self.print.setText(friends(self.token_text, self.owner_id_text))


def eternal_online(token):
    try:
        data = {'access_token': token, 'v': '5.130'}
        url = 'https://api.vk.com/method/account.setOnline?'
        while True:
            requests.get(url, data)
            time.sleep(150)
            return "Вечный онлайн включен"
    except Exception:
        return 'Error'


def account_ban(token, user_id):
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


def friends(token, owner_id):
    try:
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
