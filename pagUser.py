import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from uiPagUsuario import Ui_Dialog

class UserWindow(QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        print("Ventana cargada correctamente")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserWindow()
    window.show()
    sys.exit(app.exec_())
