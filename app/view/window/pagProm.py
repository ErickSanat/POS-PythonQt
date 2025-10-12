import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ..generated.uiPagPromocion import Ui_Form

class PromWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        print("Ventana cargada correctamente")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PromWindow()
    window.show()
    sys.exit(app.exec_())
