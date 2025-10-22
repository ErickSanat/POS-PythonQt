import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.empleadoView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado, Usuario
from app.controller import EmpleadoController, UsuarioController

class EmpleadoTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Empleado en un QTableView"""
    def __init__(self, empleados: list = None, parent=None):
        super().__init__(parent)
        self._empleados = empleados or []
        # Definir columnas: (atributo, encabezado)
        self._columns = [
            ("id_empleado", "ID"),
            ("nombre", "Nombre"),
            ("direccion", "Dirección"),
            ("telefono", "Teléfono"),
            ("usuario", "Usuario")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._empleados)

    def columnCount(self, parent=QModelIndex()):
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        empleado_obj = self._empleados[index.row()]
        attr, _header = self._columns[index.column()]

        # Manejar atributo compuesto (usuario.usuario)
        if attr == "usuario":
            usuario = getattr(empleado_obj, "usuario", None)
            return usuario.usuario if usuario else ""

        # Obtener valor del atributo
        valor = getattr(empleado_obj, attr, "")
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

    def setEmpleados(self, empleados: list):
        """Actualizar la lista de empleados en el modelo"""
        self.beginResetModel()
        self._empleados = empleados or []
        self.endResetModel()

class EmpWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)
        self.empleadoController = EmpleadoController()
        self.usuarioController = UsuarioController()
        # Llenar combobox de usuarios
        for usuario in self.usuarioController.usuarios():
            self.comboUsuario.addItem(usuario.usuario, usuario.id_usuario)

        # Llenar el combo de categorías de búsqueda
        self.comboCategorias.addItem("ID", "id_empleado")
        self.comboCategorias.addItem("Nombre", "nombre")
        self.comboCategorias.addItem("Dirección", "direccion")
        self.comboCategorias.addItem("Teléfono", "telefono")
        self.comboCategorias.addItem("Usuario", "usuario")

        # Configurar el modelo para la tabla
        self._table_model = EmpleadoTableModel()
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
        empleado = Empleado(
            nombre=self.lineNombreEmpleado.text().strip(),
            direccion=self.lineDireccionEmpleado.text().strip(),
            telefono=int(self.lineTelefonoEmpleado.text().strip()),
            usuario=Usuario(self.comboUsuario.currentData())
        )
        mensaje = self.empleadoController.addEmpleado(empleado)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()

    def handleEditarBtn(self):
        try:
            empleadoModificado = Empleado(
                id_empleado=self.empleado.id_empleado,
                nombre=self.lineNombreEmpleado.text().strip(),
                direccion=self.lineDireccionEmpleado.text().strip(),
                telefono=int(self.lineTelefono.text().strip()),
                usuario=Usuario(self.comboUsuario.currentData())
            )
            self.empleadoController.updateEmpleado(empleadoModificado)
            self.labelInformacion.setText("Empleado actualizado exitosamente")
            self.limpiarCampos()
            self.mostrarTabla()
        except Exception as e:
            self.labelInformacion.setText(f"Error al actualizar empleado: {str(e)}")

    def handleBorrarBtn(self):
        try:
            self.empleadoController.deleteEmpleado(self.empleado.id_empleado)
            self.labelInformacion.setText("Empleado eliminado exitosamente")
            self.limpiarCampos()
            self.mostrarTabla()
        except Exception as e:
            self.labelInformacion.setText(f"Error al eliminar empleado: {str(e)}")

    def handelBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            empleados = self.empleadoController.buscar(columna, aBuscar)
        except Exception:
            empleados = None
        self.lineDato.clear()
        self._table_model.setEmpleados(empleados)

    def mostrarTabla(self):
        """Cargar y mostrar los empleados en la tabla"""
        try:
            empleados = self.empleadoController.empleados()
            self._table_model.setEmpleados(empleados)
            self.empleados = None
        except Exception as e:
            print(f"Error al cargar empleados: {e}")
            self.labelInformacion.setText(f"Error al cargar empleados: {e}")

    def handleDobleClic(self, index: QModelIndex):
        datos = []
        datos.extend(
            self._table_model.index(index.row(), nColumna, index).data()
            for nColumna in range(self._table_model.columnCount())
        )

        # Llenar los campos con los datos del empleado seleccionado
        self.lineNombreEmpleado.setText(self.empleado.nombre)
        self.lineDireccionEmpleado.setText(self.empleado.direccion)
        self.lineTelefono.setText(str(self.empleado.telefono))
        self.comboUsuario.setCurrentText(self.empleado.usuario.usuario)
        if self.empleado.usuario:
            self.comboUsuario.setCurrentText(self.empleado.usuario.usuario)

    def limpiarCampos(self):
        self.lineNombreEmpleado.clear()
        self.lineDireccionEmpleado.clear()
        self.lineTelefonoEmpleado.clear()
        self.comboUsuario.setCurrentIndex(0)