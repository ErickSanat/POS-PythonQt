import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.categoriaView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado

class CatWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self,empleado: Empleado):
        super().__init__()
        self.setupUi(self)