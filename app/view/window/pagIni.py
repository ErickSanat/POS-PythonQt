import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QIcon
from ..generated.menuInicialView_ui import Ui_POS
from app.utils import MenuFlotante

class InicioWindow(QMainWindow, Ui_POS, MenuFlotante):
    def __init__(self):
        super().__init__()
        
        try:
            self.setupUi(self)
        except Exception as e:
            print(f"Advertencia al cargar la UI: {e}")
            # Continuar sin el ícono problemático
            self.setupUi(self)
        
        # ✅ CONFIGURAR EL MENÚ FLOTANTE DESPUÉS DE setupUi
        self.setupFloatingMenu()
        
        print("Ventana cargada correctamente")
        # Intentar establecer un ícono por defecto o ninguno
        self.setWindowIcon(QIcon())
