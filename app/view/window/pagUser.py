import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ..generated.usuarioview_ui import Ui_Dialog
from app.utils.menuFlotante import MenuFlotante

class UserWindow(QMainWindow, Ui_Dialog, MenuFlotante):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Configurar el menú flotante
        self.setupFloatingMenu()

        print("Ventana cargada correctamente")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserWindow()
    window.show()
    sys.exit(app.exec_())
