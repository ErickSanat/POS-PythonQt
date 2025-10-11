import sys
from PyQt5.QtWidgets import QApplication
from app import InicioSesion

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    window = InicioSesion()
    window.show()
    sys.exit(app.exec_())
