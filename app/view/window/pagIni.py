import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTabWidget, QLabel,
                             QFrame)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from ..generated.menuInicialView_ui import Ui_POS


class InicioWindow(QMainWindow, Ui_POS):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Configurar el menú flotante
        self.setupFloatingMenu()

        # Conectar el botón del menú
        if hasattr(self, 'btnMenu'):
            self.btnMenu.clicked.connect(self.toggleFloatingMenu)
        print("Ventana cargada correctamente")

    def setupFloatingMenu(self):
        """Configurar las propiedades del menú flotante"""
        # Ocultar inicialmente el menú
        self.frameFlotante.hide()

        # Configurar tamaño y posición inicial
        self.frameFlotante.setFixedSize(331, 321)

        # Conectar los botones del menú flotante
        self.connectMenuButtons()

    def connectMenuButtons(self):
        """Conectar los botones del menú flotante a sus funciones"""
        # Conectar cada botón a su función correspondiente
        buttons = {
            self.pushButton_9: self.menuInicio,  # Inicio
            self.pushButton_2: self.menuVentas,  # Ventas
            self.pushButton_3: self.menuPromociones,  # Promociones
            self.pushButton_4: self.menuClientes,  # Clientes
            self.pushButton_5: self.menuProveedores,  # Proveedores
            self.pushButton_6: self.menuProductos,  # Productos
            self.pushButton_7: self.menuRecetas,  # Recetas
            self.pushButton: self.menuEmpleados,  # Empleados
            self.pushButton_8: self.menuCerrarSesion  # Cerrar sesión
        }

        for button, function in buttons.items():
            button.clicked.connect(function)

    def toggleFloatingMenu(self):
        """Mostrar u ocultar el menú flotante"""
        if self.frameFlotante.isVisible():
            self.hideFloatingMenu()
        else:
            self.showFloatingMenu()

    def showFloatingMenu(self):
        """Mostrar el menú flotante con animación"""
        # Posicionar el menú debajo del botón
        buttonPos = self.btnMenu.pos()
        menuX = buttonPos.x() - self.frameFlotante.width() + self.btnMenu.width()
        menuY = buttonPos.y() + self.btnMenu.height() + 5

        self.frameFlotante.move(menuX, menuY)
        self.frameFlotante.show()
        self.frameFlotante.raise_()

    def hideFloatingMenu(self):
        """Ocultar el menú flotante"""
        self.frameFlotante.hide()

    def mousePressEvent(self, event):
        """Ocultar el menú flotante al hacer clic fuera de él"""
        if (self.frameFlotante.isVisible() and
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
        print("Menú: Clientes")
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
        # Aquí puedes agregar la lógica para cerrar sesión
        # self.close()

    def testFunction(self):
        print("¡El botón funciona!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InicioWindow()
    window.show()
    sys.exit(app.exec_())