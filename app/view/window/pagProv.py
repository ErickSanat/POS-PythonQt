import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.proveedorView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado, Proveedor
from app.controller import ProveedorController

class ProveedorTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Proveedor en un QTableView"""
    def __init__(self, proveedores: list = None, parent=None):
        super().__init__(parent)
        self._proveedores = proveedores or []
        # Definir columnas: (atributo, encabezado)
        self._columns = [
            ("id_proveedor", "ID"),
            ("nombre", "Nombre"),
            ("nombre_contacto", "Contacto"),
            ("telefono", "Teléfono"),
            ("direccion", "Dirección"),
            ("activo", "Activo")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._proveedores)

    def columnCount(self, parent=QModelIndex()):
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        proveedor_obj = self._proveedores[index.row()]
        attr, _header = self._columns[index.column()]

        # Manejar atributo booleano (activo)
        if attr == "activo":
            activo = getattr(proveedor_obj, "activo", None)
            return "Sí" if activo else "No"

        # Obtener valor del atributo
        valor = getattr(proveedor_obj, attr, "")
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

    def setProveedores(self, proveedores: list):
        """Actualizar la lista de proveedores en el modelo"""
        self.beginResetModel()
        self._proveedores = proveedores or []
        self.endResetModel()

class ProvWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)
        self.proveedorController = ProveedorController()
        self.proveedor = Proveedor()
        self.proveedores = None
        self.labelEmpleado.setText(f"Empleado: {empleado.nombre}")

        # Llenar el combo de proveedores
        self.rellenarCombobox()

        # Llenar el combo categorías de búsqueda
        self.comboCategorias.addItem("ID", "id_proveedor")
        self.comboCategorias.addItem("Nombre", "nombre")
        self.comboCategorias.addItem("Nombre Contacto", "nombre_contacto")
        self.comboCategorias.addItem("Teléfono", "telefono")
        self.comboCategorias.addItem("Dirección", "direccion")
        self.comboCategorias.addItem("Activo", "activo")

        # Configurar el modelo para la tabla
        self._table_model = ProveedorTableModel()
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
        self.btnBuscar.clicked.connect(self.handelBuscarBtn)

        # Configurar el menú flotante
        self.setupFloatingMenu(empleado)
        self.mostrarTabla()

    def handleAgregarBtn(self):
        if "" in [
            self.lineNombre.text().strip(),
            self.lineNombreContacto.text().strip(),
            self.lineTelefono.text().strip(),
            self.txtDireccion.toPlainText().strip()
        ]:
            print("No se puede agregar un proveedor sin datos")
            return
        proveedor = Proveedor(
            nombre=self.lineNombre.text().strip(),
            nombre_contacto=self.lineNombreContacto.text().strip(),
            telefono=self.lineTelefono.text().strip(),
            direccion=self.txtDireccion.toPlainText().strip(),
            activo=self.comboActivo.currentData()
        )
        mensaje = self.proveedorController.addProveedor(proveedor)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()
        self.rellenarCombobox()

    def handleEditarBtn(self):
        if self.proveedor.id_proveedor is None:
            return
        proveedorModificado = Proveedor(
            id_proveedor=self.proveedor.id_proveedor,
            nombre=self.lineNombre.text().strip(),
            nombre_contacto=self.lineNombreContacto.text().strip(),
            telefono=self.lineTelefono.text().strip(),
            direccion=self.txtDireccion.toPlainText().strip(),
            activo=self.comboActivo.currentData()
        )
        mensaje = self.proveedorController.updateProveedor(proveedorModificado)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()
        self.rellenarCombobox()

    def handleBorrarBtn(self):
        if self.proveedor.id_proveedor is None:
            return
        self.proveedorController.deleteProveedor(self.proveedor.id_proveedor)
        self.labelInformacion.setText("Proveedor Eliminado Exitosamente")
        self.limpiarCampos()
        self.mostrarTabla()
        self.rellenarCombobox()

    def handelBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            self.proveedores = self.proveedorController.buscar(columna, aBuscar)
        except Exception as e:
            print(f"Error al buscar: {e}")
            self.labelInformacion.setText("Error al buscar")
            self.proveedores = None
        self.lineDato.clear()
        self.mostrarTabla()

    def mostrarTabla(self):
        """Cargar y mostrar los proveedores en la tabla"""
        try:
            proveedores = self.proveedores or self.proveedorController.proveedores()
            self._table_model.setProveedores(proveedores)
            self.proveedores = None
        except Exception as e:
            print(f"Error al cargar proveedores: {e}")

    def handleDobleClic(self, index: QModelIndex):
        datos = []
        datos.extend(
            self._table_model.index(index.row(), nColumna, index).data()
            for nColumna in range(self._table_model.columnCount())
        )
        self.proveedor = Proveedor(
            id_proveedor=int(datos[0]),
            nombre=datos[1],
            nombre_contacto=datos[2],
            telefono=int(datos[3]),
            direccion=datos[4],
            activo=bool(datos[5])
        )
        self.lineNombre.setText(self.proveedor.nombre)
        self.lineNombreContacto.setText(self.proveedor.nombre_contacto)
        self.lineTelefono.setText(str(self.proveedor.telefono))
        self.txtDireccion.setText(self.proveedor.direccion)
        self.comboActivo.setCurrentText("Activo" if self.proveedor.activo else "Inactivo")

    def limpiarCampos(self):
        self.lineNombre.clear()
        self.lineNombreContacto.clear()
        self.lineTelefono.clear()
        self.txtDireccion.clear()
        self.proveedor = Proveedor()

    def rellenarCombobox(self):
        self.comboActivo.clear()
        self.comboActivo.addItem("Activo", "true")
        self.comboActivo.addItem("Inactivo", "false")