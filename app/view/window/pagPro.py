import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ..generated.productoView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado

class ProWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)

        self.setupFloatingMenu(empleado)

        print("Ventana cargada correctamente")
