import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.usuarioView_ui import Ui_Dialog
from app.utils import MenuFlotante
from app.model import Empleado, Rol, Usuario
from app.controller import UsuarioController, RolController

class UsuarioTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Usuario en un QTableView"""
    def __init__(self, usuarios: list = None, parent=None):
        super().__init__(parent)
        self._usuarios = usuarios or []
        # Definir columnas: (atributo, encabezado)
        self._columns = [
            ("id_usuario", "ID"),
            ("usuario", "Usuario"),
            ("contrasena", "Contraseña"),
            ("rol", "Rol")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._usuarios)

    def columnCount(self, parent=QModelIndex()):
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()
        
        usuario_obj = self._usuarios[index.row()]
        attr, _header = self._columns[index.column()]
        
        # Manejar atributo compuesto (rol.nombre)
        if attr == "rol":
            rol = getattr(usuario_obj, "rol", None)
            return rol.nombre if rol else ""
        
        # Obtener valor del atributo
        valor = getattr(usuario_obj, attr, "")
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

    def setUsuarios(self, usuarios: list):
        """Actualizar la lista de usuarios en el modelo"""
        self.beginResetModel()
        self._usuarios = usuarios or []
        self.endResetModel()

class UsuWindow(QMainWindow, Ui_Dialog, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.usuario = Usuario()
        self.usuarios = None
        self.setupUi(self)
        self.usuarioController = UsuarioController()
        self.rolController = RolController()
        for rol in self.rolController.roles():
            self.comboRol.addItem(rol.nombre, rol.id_rol)
            
        # ToDo: meter esto a un for para ahorrar espacio
        self.comboCategorias.addItem("ID", "id_usuario")
        self.comboCategorias.addItem("Nombre", "usuario")
        self.comboCategorias.addItem("Contraseña", "contrasena")
        self.comboCategorias.addItem("Rol", "nombre")

        # Configurar el modelo para la tabla
        self._table_model = UsuarioTableModel()
        self.tableView.setModel(self._table_model)
        
        # Configurar apariencia de la tabla
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        self.tableView.doubleClicked.connect(self.handleDobleClic)
        
        self.btnAgregar.clicked.connect(self.handleAgregarBtn)
        self.btnEditar.clicked.connect(self.handleEditarBtn)
        self.btnEliminar.clicked.connect(self.handleBorrarBtn)
        self.btnBuscar.clicked.connect(self.handelBuscarBtn)
        
        # Configurar el menú flotante
        self.setupFloatingMenu(empleado)
        self.mostrarTabla()
    
    def handleAgregarBtn(self):
        if self.lineNombreEmpleado.text().strip() == "" or self.lineContrasena.text().strip() == "":
            return
        usuario = Usuario(
            usuario=self.lineNombreEmpleado.text().strip(), 
            contrasena=self.lineContrasena.text().strip(),
            rol=Rol(self.comboRol.currentData(), self.comboRol.currentText())
        )
        mensaje = self.usuarioController.addUsuario(usuario)
        self.labelInformacion.setText(mensaje)
        self.lineNombreEmpleado.clear()
        self.lineContrasena.clear()
        
        self.mostrarTabla()

    def handleEditarBtn(self):
        if self.empleado.id_empleado is None:
            return
        usuarioModificado = Usuario(
            self.usuario.id_usuario,
            self.lineNombreEmpleado.text().strip(),
            self.lineContrasena.text().strip(),
            Rol(self.comboRol.currentData(), self.comboRol.currentText())
        )
        self.usuarioController.updateUsuario(usuarioModificado)
        self.labelInformacion.setText("Usuario Actualizado Exitosamente")
        self.lineNombreEmpleado.clear()
        self.lineContrasena.clear()
        self.mostrarTabla()
    
    def handleBorrarBtn(self):
        if self.empleado.id_empleado is None:
            return
        self.usuarioController.deleteUsuario(self.usuario.id_usuario)
        self.labelInformacion.setText("Usuario Eliminado Exitosamente")
        self.lineNombreEmpleado.clear()
        self.lineContrasena.clear()
        self.mostrarTabla()
    
    def handelBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            self.usuarios = self.usuarioController.buscar(columna, aBuscar)
        except Exception:
            self.usuarios = None
        self.lineDato.clear()
        self.mostrarTabla()
    
    def mostrarTabla(self):
        """Cargar y mostrar los usuarios en la tabla"""
        try:
            usuarios = self.usuarios or self.usuarioController.usuarios()
            self._table_model.setUsuarios(usuarios)
            self.usuarios = None
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")
    
    def handleDobleClic(self, index: QModelIndex):
        datos = []
        datos.extend(
            self._table_model.index(index.row(), nColumna, index).data()
            for nColumna in range(self._table_model.columnCount())
        )
        self.usuario = Usuario(
            datos[0],
            datos[1],
            datos[2],
            self.rolController.porNombre(datos[3])
        )
        self.lineNombreEmpleado.setText(self.usuario.usuario)
        self.lineContrasena.setText(self.usuario.contrasena)
        self.comboRol.setCurrentText(self.usuario.rol.nombre)
