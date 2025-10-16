import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ..generated.usuarioView_ui import Ui_Dialog
from app.utils import MenuFlotante

class UsuWindow(QMainWindow, Ui_Dialog, MenuFlotante):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Configurar el menú flotante
        self.setupFloatingMenu()

        print("Ventana cargada correctamente")
