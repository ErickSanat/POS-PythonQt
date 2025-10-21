import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ..generated.empleadoView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado, Usuario
from app.controller import EmpleadoController, UsuarioController

class EmpWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)
        self.empleadoController = EmpleadoController()
        self.usuarioController = UsuarioController()
        for usuario in self.usuarioController.usuarios():
            self.comboUsuario.addItem(usuario.usuario, usuario.id_usuario)
        self.setupFloatingMenu(empleado)

        print("Ventana cargada correctamente")
