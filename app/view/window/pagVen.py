import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ..generated.ventaView_ui import Ui_Form
from app.utils.menuFlotante import MenuFlotante

class VenWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setupFloatingMenu()

        print("Ventana cargada correctamente")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PromWindow()
    window.show()
    sys.exit(app.exec_())
