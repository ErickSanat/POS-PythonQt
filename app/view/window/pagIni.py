from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolButton, QSizePolicy, QSpacerItem
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
            self.setupUi(self)
        
        # Configurar el scroll area (asumiendo que se llama scrollArea)
        # Ajusta el nombre según tu UI:
        if hasattr(self, 'scrollArea'):
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Crear un widget contenedor para el grid si no existe
        if not hasattr(self, 'scrollAreaWidgetContents'):
            contenedor_widget = QWidget()
            contenedor_widget.setLayout(self.gridLayoutProductos)
            if hasattr(self, 'scrollArea'):
                self.scrollArea.setWidget(contenedor_widget)
        else:
            # Si ya existe, asegurar que tenga la política de tamaño correcta
            self.scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Llenar el grid con productos
        columnas = 5
        productos = self.productoController.productos()
        
        for indice, producto in enumerate(productos):
            fila = indice // columnas
            columna = indice % columnas
            widget_producto = ProductoWidget(producto, self.agregarAlCarrito)
            self.gridLayoutProductos.addWidget(widget_producto, fila, columna)
        
        # Agregar spacer al final para empujar el contenido hacia arriba
        filas_totales = (len(productos) + columnas - 1) // columnas
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayoutProductos.addItem(spacer, filas_totales, 0, 1, columnas)
        
        # Configurar el menú flotante
        self.setupFloatingMenu(empleado)
        
        print("Ventana cargada correctamente")
        self.setWindowIcon(QIcon())
    
    def agregarAlCarrito(self, producto: Producto):
        print(producto)

class ProductoWidget(QWidget):
    def __init__(self, producto: Producto, agregarAlCarrito):
        super().__init__()
        
        # Establecer política de tamaño fija para evitar expansión descontrolada
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFixedSize(120, 135)
        
        boton = QToolButton()
        boton.setText(
            f"{producto.nombre}"
            + f"\n Stock: {producto.stock}")
        boton.setIcon(QIcon(producto.imagen))
        boton.setIconSize(QSize(80, 80))
        boton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        boton.setMinimumSize(120, 135)
        boton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        boton.setStyleSheet("""
    QToolButton {
        border: 1px solid #ccc;
        border-radius: 8px;
        padding-top: 5px;
        padding-bottom: 5px;
        background-color: #f9f9f9;
        font-size: 16px;
        qproperty-iconSize: 80px;
    }
    QToolButton:hover {
        background-color: #e0f7fa;
        border: 2px solid #26a69a;
    }
    QToolButton:pressed {
        background-color: #b2dfdb;
    }
""")

        boton.clicked.connect(lambda: agregarAlCarrito(producto))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(boton)
        self.setLayout(layout)
