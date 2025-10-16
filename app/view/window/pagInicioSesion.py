from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ..generated.inicioSesionView_ui import Ui_InicioSesion
from .pagIni import InicioWindow
from app.model import Empleado, Usuario, Rol


class InicioSesion(QMainWindow, Ui_InicioSesion):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnIngresar.clicked.connect(self.login)
        self.lineContrasena.returnPressed.connect(self.login)
        
    def lanzarPagIni(self):
        self.hide()
        self.pagIni = InicioWindow(
            Empleado(1, "jose el admin", "aki mismo", 4568542348, 
                    Usuario(1, "admin", "admin", Rol(1, "empleado")))
        )
        self.pagIni.show()

    def login(self):
        username = self.lineNombre.text().strip()
        password = self.lineContrasena.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        if username == "admin" and password == "admin":
            self.lanzarPagIni()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")
