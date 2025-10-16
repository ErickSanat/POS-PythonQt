from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ..generated.inicioSesionView_ui import Ui_InicioSesion
from .pagIni import InicioWindow


class InicioSesion(QMainWindow, Ui_InicioSesion):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.payButton_5.clicked.connect(self.login)

    def lanzarPagIni(self):
        self.hide()
        self.pagIni = InicioWindow()
        self.pagIni.show()

    def login(self):
        username = self.user_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        if username == "admin" and password == "admin":
            self.lanzarPagIni()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")
