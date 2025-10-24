import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QToolButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

from ..generated.menuInicialView_ui import Ui_POS
from app.utils import MenuFlotante
from app.model import Empleado, Producto
from app.controller import ProductoController

class InicioWindow(QMainWindow, Ui_POS, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.productoController = ProductoController()
        try:
            self.setupUi(self)
        except Exception as e:
            print(f"Advertencia al cargar la UI: {e}")
            # Continuar sin el ícono problemático
            self.setupUi(self)
        
        columnas = 6
        for indice, producto in enumerate(self.productoController.productos()):
            fila = indice // columnas
            columna = indice % columnas
            self.gridLayoutProductos.addWidget(ProductoWidget(producto, self.agregarAlCarrito), fila, columna)
        # ✅ CONFIGURAR EL MENÚ FLOTANTE DESPUÉS DE setupUi
        self.setupFloatingMenu(empleado)
        
        print("Ventana cargada correctamente")
        # Intentar establecer un ícono por defecto o ninguno
        self.setWindowIcon(QIcon())
    
    def agregarAlCarrito(self, producto: Producto):
        print(producto)

class ProductoWidget(QWidget):
    def __init__(self, producto: Producto, agregarAlCarrito):
        super().__init__()        
        boton = QToolButton()
        boton.setText(producto.nombre)
        boton.setIcon(QIcon(producto.imagen))
        boton.setIconSize(QSize(80, 80))
        boton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 👈 texto debajo del ícono
        # boton.setMinimumSize(100, 120)
        boton.setMaximumSize(120, 120)
        boton.setSizePolicy(boton.sizePolicy().Expanding, boton.sizePolicy().Expanding)
        
        boton.setStyleSheet("""
    QToolButton {
        border: 1px solid #ccc;
        border-radius: 8px;
        padding-top: 5px;
        padding-bottom: 5px;
        background-color: #f9f9f9;
        font-size: 12px;
        qproperty-iconSize: 80px;
    }
    QToolButton:hover {
        background-color: #e0f7fa;
    }
""")

        boton.clicked.connect(lambda: agregarAlCarrito(producto.nombre))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(boton)
        self.setLayout(layout)
