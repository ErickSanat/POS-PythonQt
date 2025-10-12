import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtGui import QIcon
from ..generated.menuInicialView_ui import Ui_POS
from .pagUser import UserWindow


class InicioWindow(QMainWindow, Ui_POS):
    def __init__(self):
        super().__init__()
        try:
            self.setupUi(self)
        except Exception as e:
            print(f"Advertencia al cargar la UI: {e}")
            # Continuar sin el ícono problemático
            self.setupUi(self)
        
        # Intentar establecer un ícono por defecto o ninguno
        self.setWindowIcon(QIcon())

        # Configurar el menú flotante
        self.setupFloatingMenu()

        # Conectar el botón del menú
        if hasattr(self, 'btnMenu'):
            self.btnMenu.clicked.connect(self.toggleFloatingMenu)
        print("Ventana cargada correctamente")

    def setupFloatingMenu(self):
        """Configurar las propiedades del menú flotante"""
        # Verificar que el frameFlotante existe antes de usarlo
        if not hasattr(self, 'frameFlotante'):
            print("Advertencia: frameFlotante no existe")
            return
            
        # Ocultar inicialmente el menú
        self.frameFlotante.hide()

        # Configurar tamaño y posición inicial
        self.frameFlotante.setFixedSize(331, 321)

        # Conectar los botones del menú flotante
        self.connectMenuButtons()

    def connectMenuButtons(self):
        """Conectar los botones del menú flotante a sus funciones"""
        # Verificar que todos los botones existen antes de conectarlos
        button_mappings = {
            'btnMenuInicio': self.menuInicio,
            'btnVentas': self.menuVentas,
            'btnPromociones': self.menuPromociones,
            'btnClientes': self.menuClientes,
            'btnProveedores': self.menuProveedores,
            'btnProductos': self.menuProductos,
            'btnRecetas': self.menuRecetas,
            'btnEmpleados': self.menuEmpleados,
            'btnCerrarSesion': self.menuCerrarSesion
        }

        for button_name, function in button_mappings.items():
            if hasattr(self, button_name):
                button = getattr(self, button_name)
                button.clicked.connect(function)
            else:
                print(f"Advertencia: Botón {button_name} no encontrado")

    def toggleFloatingMenu(self):
        """Mostrar u ocultar el menú flotante"""
        if not hasattr(self, 'frameFlotante'):
            return
            
        if self.frameFlotante.isVisible():
            self.hideFloatingMenu()
        else:
            self.showFloatingMenu()

    def showFloatingMenu(self):
        """Mostrar el menú flotante con animación"""
        if not hasattr(self, 'frameFlotante') or not hasattr(self, 'btnMenu'):
            return
            
        # Posicionar el menú debajo del botón
        buttonPos = self.btnMenu.pos()
        menuX = buttonPos.x() - self.frameFlotante.width() + self.btnMenu.width()
        menuY = buttonPos.y() + self.btnMenu.height() + 5

        self.frameFlotante.move(menuX, menuY)
        self.frameFlotante.show()
        self.frameFlotante.raise_()

    def hideFloatingMenu(self):
        """Ocultar el menú flotante"""
        if hasattr(self, 'frameFlotante'):
            self.frameFlotante.hide()

    def mousePressEvent(self, event):
        """Ocultar el menú flotante al hacer clic fuera de él"""
        if (hasattr(self, 'frameFlotante') and hasattr(self, 'btnMenu') and
                self.frameFlotante.isVisible() and
                not self.frameFlotante.geometry().contains(event.globalPos()) and
                not self.btnMenu.geometry().contains(self.btnMenu.mapFromGlobal(event.globalPos()))):
            self.hideFloatingMenu()
        super().mousePressEvent(event)

    # Funciones para los botones del menú
    def menuInicio(self):
        print("Menú: Inicio")
        self.hideFloatingMenu()

    def menuVentas(self):
        print("Menú: Ventas")
        self.hideFloatingMenu()

    def menuPromociones(self):
        print("Menú: Promociones")
        self.hideFloatingMenu()

    def menuClientes(self):
        self.pagUser = UserWindow()
        self.pagUser.show()
        self.hideFloatingMenu()

    def menuProveedores(self):
        print("Menú: Proveedores")
        self.hideFloatingMenu()

    def menuProductos(self):
        print("Menú: Productos")
        self.hideFloatingMenu()

    def menuRecetas(self):
        print("Menú: Recetas")
        self.hideFloatingMenu()

    def menuEmpleados(self):
        print("Menú: Empleados")
        self.hideFloatingMenu()

    def menuCerrarSesion(self):
        print("Menú: Cerrar sesión")
        self.hideFloatingMenu()
        QApplication.quit()

    def testFunction(self):
        print("¡El botón funciona!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InicioWindow()
    window.show()
    sys.exit(app.exec_())