from PyQt5.QtWidgets import QMainWindow, QMessageBox
from ..generated.ui_login import Ui_InicioSesion
from .pagIni import TestWindow
class InicioSesion(QMainWindow, Ui_InicioSesion):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.payButton_5.clicked.connect(self.lanzarPagIni)

    def lanzarPagIni(self):
        self.hide()
        self.pagIni = TestWindow()
        self.pagIni.show()

    def login(self):
        """Manejar el evento de login"""
        username = self.user_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return
        
        # Aquí va tu lógica de autenticación
        if username == "admin" and password == "admin":
            QMessageBox.information(self, "Éxito", "¡Inicio de sesión exitoso!")
            # Aquí puedes abrir la ventana principal
            # self.open_main_window()
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")
    
    def open_main_window(self):
        """Abrir ventana principal (para implementar después)"""
        # self.hide()
        # self.main_window = MainWindow()
        # self.main_window.show()
        pass
