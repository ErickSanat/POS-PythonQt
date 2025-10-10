import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from app import InicioSesion
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Establecer estilo global
    app.setStyle('Fusion')
    
    window = InicioSesion()
    window.show()
    sys.exit(app.exec_())
