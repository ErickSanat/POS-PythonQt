import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Importar la interfaz generada
from app import Ui_InicioSesion

class InicioSesion(QMainWindow, Ui_InicioSesion):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Establecer estilo global
    app.setStyle('Fusion')
    
    window = InicioSesion()
    window.show()
    sys.exit(app.exec_())
