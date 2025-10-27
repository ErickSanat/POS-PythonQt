import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.ventaView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Venta, Empleado, Cliente, Promocion, Pago
from app.controller import (VentaController, EmpleadoController,
                            ClienteController, PromocionController,
                            PagoController)

class VentaTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Venta en un QTableView"""
    def __init__(self, ventas: list = None, parent=None):
        super().__init__(parent)
        self.ventas = ventas or []
        # Definir columnas: (atributo, encabezado)
        self._columns = [
            ("id_venta", "ID"),
            ("fecha", "Fecha"),
            ("empleado", "Empleado"),
            ("cliente", "Cliente"),
            ("promocion", "Promocion"),
            ("pago", "Pago"),
            ("total", "Total")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self.ventas)

    def columnCount(self, parent=QModelIndex()):
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        venta_obj = self.ventas[index.row()]
        attr, _header = self._columns[index.column()]

        # Manejar atributo compuesto (empleado.nombre)
        if attr == "empleado":
            empleado = getattr(venta_obj, "empleado", None)
            return str(empleado.nombre) if empleado is not None else ""

        # Manejar atributo compuesto (cliente.nombre)
        if attr == "cliente":
            cliente = getattr(venta_obj, "cliente", None)
            return str(cliente.nombre) if cliente is not None else ""

        # Manejar atributo compuesto (promocion.nombre)
        if attr == "promocion":
            promocion = getattr(venta_obj, "promocion", None)
            return str(promocion.nombre) if promocion is not None else ""

        # Manejar atributo compuesto (pago.metodo)
        if attr == "pago":
            pago = getattr(venta_obj, "pago", None)
            return str(pago.metodo) if pago is not None else ""

        # Obtener valor del atributo
        valor = getattr(venta_obj, attr, "")
        return str(valor) if valor is not None else ""

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

    def setVentas(self, ventas: list):
        """Actualizar la lista de ventas en el modelo"""
        self.beginResetModel()
        self.ventas = ventas or []
        self.endResetModel()

class VenWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)
        self.ventaController = VentaController()
        self.clienteController = ClienteController()
        self.empleadoController = EmpleadoController()
        self.promocionController = PromocionController()
        self.pagoController = PagoController()
        self.venta = Venta()
        self.ventas = None

        # Llenar combobox de de categorias de busqueda
        self.comboCategorias.addItem("ID", "id_venta")
        self.comboCategorias.addItem("Fecha", "fecha")
        self.comboCategorias.addItem("Empleado", "empleado")
        self.comboCategorias.addItem("Cliente", "cliente")
        self.comboCategorias.addItem("Promocion", "promocion")
        self.comboCategorias.addItem("Pago", "pago")
        self.comboCategorias.addItem("Total", "total")

        # Configurar el modelo para la tabla
        self._table_model = VentaTableModel()
        self.tableView.setModel(self._table_model)

        # Configurar apariencia de la tabla
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        #self.tableView.doubleClicked.connect(self.handleDobleClic)

        # Conectar botones
        self.btnBuscar.clicked.connect(self.handleBuscarBtn)

        # Configurar el menú flotante
        self.setupFloatingMenu(empleado)
        self.mostrarTabla()

    def handleBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            self.ventas = self.ventaController.buscar(columna, aBuscar)
        except Exception:
            self.labelInformacion.setText("Error al buscar")
        else:
            self.lineDato.clear()
            self.mostrarTabla()

    def mostrarTabla(self):
        """Cargar y mostrar las ventas en la tabla"""
        try:
            ventas = self.ventas or self.ventaController.ventas()
            self._table_model.setVentas(ventas)
        except Exception as e:
            self.labelInformacion.setText("Error al cargar ventas")