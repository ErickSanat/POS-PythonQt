from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QToolButton, QSizePolicy,
    QSpacerItem, QHBoxLayout, QPushButton, QLabel
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QAbstractTableModel, QSize, QModelIndex, QVariant

from ..generated.menuInicialView_ui import Ui_POS
from app.utils import MenuFlotante, generarTicket
from app.model import Empleado, Producto, DetalleVenta, Venta, Cliente, Pago, Promocion, TipoPago
from app.controller import ProductoController, ClienteController, PromocionController, TipoPagoController, PagoController, VentaController, DetalleVentaController

from datetime import datetime


class DetalleVentaTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos DetalleVenta en un QTableView"""
    def __init__(self, detalleVenta: list[DetalleVenta] = None, parent=None):
        super().__init__(parent)
        self._detalleVenta = detalleVenta or []
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

        if attr == "producto":
            if role == Qt.DisplayRole:
                producto = getattr(detalleVenta, "producto", None)
                return producto.nombre if producto else ""
            return QVariant()

        if attr == "precio":
            if role == Qt.DisplayRole:
                producto = getattr(detalleVenta, "producto", None)
                return str(producto.precio) if producto else "0"
            return QVariant()

        if attr == "subtotal":
            if role == Qt.DisplayRole:
                subtotal = getattr(detalleVenta, "subtotal", None)
                return str(subtotal) if subtotal else "0"
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
        self.clienteController = ClienteController()
        self.promocionController = PromocionController()
        self.tipoPagoController = TipoPagoController()
        self.pagoController = PagoController()
        self.ventaController = VentaController()
        self.detalleVentaController = DetalleVentaController()
        self.detalleVentas: list[DetalleVenta] = []
        self.venta = None
        self.empleado = empleado

        try:
            self.setupUi(self)
        except Exception as e:
            print(f"Advertencia al cargar la UI: {e}")
            self.setupUi(self)

        # Configurar scroll area (si existe en UI)
        if hasattr(self, 'scrollArea'):
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Asegurar que el widget contenedor del scroll use el gridLayoutProductos
        if not hasattr(self, 'scrollAreaWidgetContents'):
            contenedor_widget = QWidget()
            contenedor_widget.setLayout(self.gridLayoutProductos)
            if hasattr(self, 'scrollArea'):
                self.scrollArea.setWidget(contenedor_widget)
        else:
            self.scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Llenar grid con productos
        columnas = 5
        productos: list[Producto] = []
        try:
            productos = self.productoController.productos()
        except Exception:
            productos = []

        for indice, producto in enumerate(productos):
            fila = indice // columnas
            columna = indice % columnas
            widget_producto = ProductoWidget(producto, self.agregarAlCarrito)
            self.gridLayoutProductos.addWidget(widget_producto, fila, columna)

        # Spacer final para empujar contenido hacia arriba cuando hay pocas filas
        filas_totales = (len(productos) + columnas - 1) // columnas
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayoutProductos.addItem(spacer, filas_totales, 0, 1, columnas)

        # Configurar modelo y TableView
        self._table_model = DetalleVentaTableModel()
        self.tableView.setModel(self._table_model)
        # reinstalar widgets en la columna "cantidad" cada vez que el modelo se resetee
        self._table_model.modelReset.connect(self.handleCantidadBtns)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        self.tableView.doubleClicked.connect(self.handleDobleClic)
        
        self.chkBoxDescuento.stateChanged.connect(self.handlePromocionChk)
        # self.chkBoxTicket.stateChanged.connect(self.handlePromocionChk)
        self.btnLimpiarVenta.clicked.connect(self.handleLimpiarBtn)
        self.btnLimpiarPago.clicked.connect(self.handleRealizarPago)

        # Menú flotante
        self.setupFloatingMenu(empleado)

        self.rellenarComboClientes()
        self.rellenarComboDescuentos()
        self.rellenarComboFormaPago()
        print("Ventana cargada correctamente")
        self.setWindowIcon(QIcon())

    def agregarAlCarrito(self, producto: Producto):
        cantidad = 1
        if self.venta is None:
            self.venta = Venta(
                None,
                datetime.now().isoformat(" ", "seconds"),
                self.empleado,
                Cliente(
                    self.comboClientes.currentData() if self.comboClientes.currentData() != "" else None,
                    self.comboClientes.currentText() if self.comboClientes.currentText() != "" else None
                ),
                Promocion(),
                Pago(tipo_pago=TipoPago()),
                0
            )

        for detalleVenta in self.detalleVentas:
            if producto.id_producto == detalleVenta.producto.id_producto:
                if detalleVenta.cantidad < producto.stock:
                    detalleVenta.cantidad += cantidad
                    detalleVenta.subtotal = detalleVenta.cantidad * detalleVenta.producto.precio
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
        """Actualizar tabla con self.detalleVentas"""
        try:
            if self.venta:
                self.venta.total = float(sum(x.subtotal for x in self.detalleVentas))
                self.labelSubtotal.setText(f"Subtotal: ${self.venta.total:.2f}")
                descuento = 0
                if self.venta.promocion.id_promocion:
                    descuento = self.venta.total * (self.venta.promocion.porcentaje / 100)
                
                self.labelDescuentoMostrado.setText(f"Descuento: ${descuento:.2f}")
                self.labelTotalMostrado.setText(f"TOTAL: ${self.venta.total - descuento:.2f}")
                self.venta.total -= descuento
            self._table_model.setDetalleVentas(self.detalleVentas)
            # asegurar instalación de los widgets en la columna 'cantidad'
            self.handleCantidadBtns()
        except Exception as e:
            # print(f"Error al cargar detalleVenta: {e}")
            raise e

    def handleCantidadBtns(self):
        """Instala en cada fila el widget [-] [valor] [+] en la columna 'cantidad'."""
        col_cantidad = 2  # según _columns en DetalleVentaTableModel
        row_count = self._table_model.rowCount()
        if row_count == 0:
            return

        for row in range(row_count):
            idx = self._table_model.index(row, col_cantidad)
            # crear contenedor horizontal
            w = QWidget()
            h = QHBoxLayout(w)
            h.setContentsMargins(2, 2, 2, 2)
            h.setSpacing(4)

            # botón izquierdo "-"
            btnRestar = QPushButton("-")
            btnRestar.setFixedWidth(28)
            btnRestar.setProperty("row", row)
            btnRestar.clicked.connect(lambda _=None, r=row: self.handleRestarBtn(r))

            # label central que muestra el valor
            valor = self._table_model.data(idx, Qt.DisplayRole)
            val = QLabel(str(valor))
            val.setProperty("row", row)
            val.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            val.setAlignment(Qt.AlignCenter)

            # botón derecho "+"
            btnSumar = QPushButton("+")
            btnSumar.setFixedWidth(28)
            btnSumar.setProperty("row", row)
            btnSumar.clicked.connect(lambda _=None, r=row: self.handleAgregarBtn(r))

            h.addWidget(btnRestar)
            h.addWidget(val)
            h.addWidget(btnSumar)

            # instalar widget en la vista (reemplaza la celda)
            self.tableView.setIndexWidget(idx, w)

    def handleRestarBtn(self, row: int):
        """Acción ejemplo para botón izquierdo: decrementar cantidad."""
        try:
            detalle = self.detalleVentas[row]
            if detalle.cantidad > 1:
                detalle.cantidad -= 1
                detalle.subtotal = detalle.producto.precio * detalle.cantidad
            else:
                self.detalleVentas.remove(detalle)
            
            self.mostrarTabla()
        except Exception as e:
            print(f"Error en handleRestarBtn: {e}")

    def handleAgregarBtn(self, row: int):
        """Acción ejemplo para botón derecho: incrementar cantidad."""
        try:
            detalle = self.detalleVentas[row]
            if detalle.cantidad < detalle.producto.stock:
                detalle.cantidad += 1
            detalle.subtotal = detalle.producto.precio * detalle.cantidad
            self.mostrarTabla()
        except Exception as e:
            print(f"Error en handleAgregarBtn: {e}")

    def handlePromocionChk(self):
        if not self.venta:
            return

        self.venta.promocion = self.promocionController.promocion(
                    self.comboDescuentos.currentData()
                ) if self.chkBoxDescuento.isChecked() else Promocion()
        self.mostrarTabla()

    def handleDobleClic(self, index: QModelIndex):
        detalle = self.detalleVentas[index.row()]
        self.detalleVentas.remove(detalle)
        self.mostrarTabla()
    
    def handleLimpiarBtn(self):
        self.detalleVentas = []
        self.venta = None
        self.chkBoxDescuento.setChecked(False)
        self.limpiarLabels()
        self.mostrarTabla()
    
    def handleRealizarPago(self):
        if not self.venta:
            return
        
        if not self.detalleVentas:
            return
        # print(self.venta)
        pago = Pago(
            None,
            TipoPago(self.comboFormaPago.currentData()),
            self.venta.total
        )
        self.pagoController.addPago(pago)
        self.venta.pago = self.pagoController.ultimoPago()
        
        self.ventaController.addVenta(self.venta)
        self.venta = self.ventaController.ultimoVenta()
        
        for detalle in self.detalleVentas:
            detalle.venta = self.venta
            self.detalleVentaController.addDetalleVenta(detalle)
        if self.chkBoxTicket.isChecked():
            generarTicket(f"ticket_{self.venta.id_venta}.pdf", self.detalleVentas)
        self.handleLimpiarBtn()

    def rellenarComboClientes(self):
        self.comboClientes.clear()
        for cliente in self.clienteController.clientes():
            self.comboClientes.addItem(cliente.nombre, cliente.id_cliente)

    def rellenarComboDescuentos(self):
        self.comboDescuentos.clear()
        for descuento in self.promocionController.promociones():
            self.comboDescuentos.addItem(descuento.nombre, descuento.id_promocion)
    
    def rellenarComboFormaPago(self):
        self.comboFormaPago.clear()
        for forma in self.tipoPagoController.tiposPago():
            self.comboFormaPago.addItem(forma.nombre, forma.id_tipo_pago)

    def limpiarLabels(self):
        self.labelSubtotal.setText(f"Subtotal: ${0:.2f}")
        self.labelDescuentoMostrado.setText(f"Descuento: ${0:.2f}")
        self.labelTotalMostrado.setText(f"TOTAL: ${0:.2f}")

class ProductoWidget(QWidget):
    """Widget-botón para producto: sigue siendo clickable y su contenido queda pegado abajo."""
    def __init__(self, producto: Producto, agregarAlCarrito):
        super().__init__()

        # Contenedor tamaño fijo para cuadrícula uniforme
        self.setFixedSize(120, 135)

        boton = QToolButton()
        boton.setText(f"{producto.nombre}\nStock: {producto.stock}")
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
                    text-align: center;
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
                    text-align: center;
                }
            """)

        # Layout: spacer arriba empuja el botón hacia el borde inferior del contenedor
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(boton)
        self.setLayout(layout)
