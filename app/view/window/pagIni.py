from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QToolButton, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QAbstractTableModel, QSize, QModelIndex, QVariant

from ..generated.menuInicialView_ui import Ui_POS
from app.utils import MenuFlotante
from app.model import Empleado, Producto, DetalleVenta, Venta
from app.controller import ProductoController

from datetime import datetime


class DetalleVentaTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Producto en un QTableView"""
    def __init__(self, detalleVenta: list[DetalleVenta] = None, parent=None):
        super().__init__(parent)
        self._detalleVenta = detalleVenta or []
        # Ajusta columnas según atributos reales de tu modelo Producto
        self._columns = [
            ("producto", "Producto"),
            ("precio", "Precio"),
            ("cantidad", "Cantidad"),
            ("subtotal", "Subtotal")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._detalleVenta)

    def columnCount(self, parent=QModelIndex()):
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        detalleVenta = self._detalleVenta[index.row()]
        attr, _header = self._columns[index.column()]

        # Manejo especial para la columna "producto"
        if attr == "producto":
            if role == Qt.DisplayRole:
                producto = getattr(detalleVenta, "producto", None)
                return producto.nombre if producto else ""
            return QVariant()
        
        # Manejo especial para la columna "precio"
        if attr == "precio":
            if role == Qt.DisplayRole:
                producto = getattr(detalleVenta, "producto", None)
                return str(producto.precio) if producto else ""
            return QVariant()
        
        # Manejo especial para la columna "subtotal"
        if attr == "subtotal":
            if role == Qt.DisplayRole:
                producto = getattr(detalleVenta, "producto", None)
                return str(producto.precio * detalleVenta.cantidad) if producto else ""
            return QVariant()

        if role == Qt.DisplayRole:
            valor = getattr(detalleVenta, attr, "")
            return str(valor) if valor is not None else ""
        
        return QVariant()
        

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return self._columns[section][1]
        return str(section + 1)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setDetalleVentas(self, detalleVenta: list[DetalleVenta]):
        self.beginResetModel()
        self._detalleVenta = detalleVenta or []
        self.endResetModel()


class InicioWindow(QMainWindow, Ui_POS, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.productoController = ProductoController()
        self.detalleVentas: list[DetalleVenta] = []
        self.venta = None
        self.empleado = empleado
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
        
        # ToDo: meter esto a una funcion para actualizar cada que se realice una compra
        for indice, producto in enumerate(productos):
            fila = indice // columnas
            columna = indice % columnas
            widget_producto = ProductoWidget(producto, self.agregarAlCarrito)
            self.gridLayoutProductos.addWidget(widget_producto, fila, columna)
        
        # Agregar spacer al final para empujar el contenido hacia arriba
        filas_totales = (len(productos) + columnas - 1) // columnas
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayoutProductos.addItem(spacer, filas_totales, 0, 1, columnas)
        
        # Configurar el modelo para la tabla
        self._table_model = DetalleVentaTableModel()
        self.tableView.setModel(self._table_model)
        
        # Configurar apariencia de la tabla
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        # Configurar el menú flotante
        self.setupFloatingMenu(empleado)
        
        print("Ventana cargada correctamente")
        self.setWindowIcon(QIcon())
    
    def agregarAlCarrito(self, producto: Producto):
        cantidad = 1
        if self.venta is None:
            self.venta = Venta(
                None,
                datetime.now(),
                self.empleado.usuario,
                self.comboFormaPago.currentData() if self.comboFormaPago.currentData() != "" else None,
                0
            )
        
        for detalleVenta in self.detalleVentas:
            if producto.id_producto == detalleVenta.producto.id_producto:
                detalleVenta.cantidad += cantidad
                self.mostrarTabla()
                return
                
        self.detalleVentas.append(
            DetalleVenta(
                None,
                self.venta,
                producto,
                cantidad,
                producto.precio * cantidad
            )
        )
        self.mostrarTabla()
    
    def mostrarTabla(self):
        """Cargar y mostrar los detalleVenta en la tabla"""
        try:
            detalleVenta = self.detalleVentas or self.detalleVentaController.detalleVenta()
            self._table_model.setDetalleVentas(detalleVenta)
        except Exception as e:
            print(f"Error al cargar detalleVenta: {e}")

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
        
        if producto.stock != 0:
            boton.setStyleSheet("""
                QToolButton {
                    border: 2px solid #867BAA;
                    border-radius: 8px;
                    padding-top: 5px;
                    padding-bottom: 5px;
                    background-color: #CFC3F5;
                    font-size: 16px;
                    qproperty-iconSize: 80px;
                }
                QToolButton:hover {
                    background-color: #DED8EF;
                }
                QToolButton:pressed {
                    background-color: #988DBD;
                }
            """)
            
            boton.clicked.connect(lambda: agregarAlCarrito(producto))
        else:
            boton.setStyleSheet("""
                QToolButton {
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    padding-top: 5px;
                    padding-bottom: 5px;
                    background-color: #d6d6d6;
                    font-size: 16px;
                    qproperty-iconSize: 80px;
                }
            """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(boton)
        self.setLayout(layout)
