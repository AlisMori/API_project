import sys
import traceback
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5 import uic


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
        self.function1.clicked.connect(self.functions)

    def functions(self):
        pass

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
        pass


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)


sys.excepthook = excepthook
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
