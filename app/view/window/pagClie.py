import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.clienteView_ui import Ui_Dialog
from app.utils import MenuFlotante
from app.model import Empleado, Cliente
from app.controller import ClienteController

class ClienteTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Cliente en un QTableView"""
    def __init__(self, clientes: list = None, parent=None):
        super().__init__(parent)
        self._clientes = clientes or []
        # Definir columnas: (atributo, encabezado)
        self._colums = [
            ("id_cliente", "ID"),
            ("nombre", "Nombre"),
            ("telefono", "Télefono"),
            ("correo", "Correo")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._clientes)

    def columnCount(self, parent=QModelIndex()):
        return len(self._colums)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        cliente_obj = self._clientes[index.row()]
        attr, _header = self._colums[index.column()]

        # Manejar atributo compuesto (rol.nombre)
        if attr == "rol":
            valor = getattr(cliente_obj, "rol", None)
            return rol.nombre if rol else ""

        # Obtener valor del atributo
        valor = getattr(cliente_obj, attr, "")
        return str(valor) if valor is not None else ""

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            return self._colums[section][1]

        return str(section + 1)

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setClientes(self, clientes: list):
        """Actualizar la lista de clientes en el modelo"""
        self.beginResetModel()
        self._clientes = clientes or []
        self.endResetModel()

class CliWindow(QMainWindow, Ui_Dialog, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)
        self.clienteController = ClienteController()
        self.cliente = Cliente()
        self.clientes = None

        self.comboCategorias.addItem("ID", "id_cliente")
        self.comboCategorias.addItem("Nombre", "nombre")
        self.comboCategorias.addItem("Teléfono", "telefono")
        self.comboCategorias.addItem("Correo", "correo")


        # Configurar el modelo para la tabla
        self._table_model = ClienteTableModel()
        self.tableView.setModel(self._table_model)

        # Configurar apariencia de la tabla
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        self.tableView.doubleClicked.connect(self.handleDobleClic)

        # Conectar botones
        self.btnAgregar.clicked.connect(self.handleAgregarBtn)
        self.btnEditar.clicked.connect(self.handleEditarBtn)
        self.btnEliminar.clicked.connect(self.handleBorrarBtn)
        self.btnBuscar.clicked.connect(self.handleBuscarBtn)

        # Configurar el menú flotante
        self.setupFloatingMenu(empleado)
        self.mostrarTabla()

    def handleAgregarBtn(self):
         if "" in [
            self.lineNombre.text().strip(),
            self.lineTelefono.text().strip(),
            self.lineCorreo.text().strip()
         ]:
             print("No se puede agregar un cliente sin datos")
             return
         cliente = Cliente(
             nombre=self.lineNombre.text().strip(),
             telefono=self.lineTelefono.text().strip(),
             correo=self.lineCorreo.text().strip(),
         )
         mensaje = self.clienteController.addCliente(cliente)
         self.labelInformacion.setText(mensaje)
         self.limpiarCampos()
         self.mostrarTabla()

    def handleEditarBtn(self):
        if self.cliente.id_cliente is None:
            return
        clienteModificado = Cliente(
            id_cliente=self.cliente.id_cliente,
            nombre=self.lineNombre.text().strip(),
            telefono=self.lineTelefono.text().strip(),
            correo=self.lineCorreo.text().strip(),
        )
        mensaje = self.clienteController.updateCliente(clienteModificado)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()

    def handleBorrarBtn(self):
        if self.cliente.id_cliente is None:
            return
        mensaje = self.clienteController.deleteCliente(self.cliente.id_cliente)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()

    def handleBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            self.clientes = self.clienteController.buscar(columna, aBuscar)
        except Exception as e:
            self.labelInformacion.setText("Error al buscar")
            self.clientes = None
        self.lineDato.clear()
        self.mostrarTabla()

    def handleDobleClic(self, index: QModelIndex):
        datos = []
        datos.extend(
            self._table_model.index(index.row(), nColumna, index).data()
            for nColumna in range(self._table_model.columnCount())
        )
        self.cliente = Cliente(
            id_cliente=datos[0],
            nombre=datos[1],
            telefono=datos[2],
            correo=datos[3]
        )
        self.lineNombre.setText(self.cliente.nombre)
        self.lineTelefono.setText(str(self.cliente.telefono))
        self.lineCorreo.setText(self.cliente.correo)

    def mostrarTabla(self):
        """Cargar y mostrar los clientes en la tabla"""
        try:
            clientes = self.clientes or self.clienteController.clientes()
            self._table_model.setClientes(clientes)
            self.clientes = None
        except Exception as e:
            print(f"Error al cargar clientes: {e}")

    def limpiarCampos(self):
        self.lineNombre.clear()
        self.lineTelefono.clear()
        self.lineCorreo.clear()
        self.cliente = Cliente()