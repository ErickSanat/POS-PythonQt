import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

# Importar la interfaz generada
from ui_login import Ui_LoginWindow

class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Configurar la imagen del logo
        self.setup_logo()
        
        # Conectar señales
        self.login_button.clicked.connect(self.login)
        
    def setup_logo(self):
        """Configurar la imagen del logo"""
        logo_path = "logoPasteleria.png"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                # Escalar manteniendo aspecto
                scaled_pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(scaled_pixmap)
                self.logo_label.setAlignment(Qt.AlignCenter)
            else:
                self.setup_text_logo()
        else:
            self.setup_text_logo()
    
    def setup_text_logo(self):
        """Mostrar texto si no hay imagen"""
        self.logo_label.setText("ALQUIMIA\nPASTELERÍA")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 24px;
                font-weight: bold;
                padding: 20px;
            }
        """)
    
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
    
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
