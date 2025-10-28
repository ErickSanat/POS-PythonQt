import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.categoriaView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado, Categoria
from app.controller import CategoriaController

class CategoriaTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Categoria en un QTableView"""
    def __init__(self, categorias: list = None, parent=None):
        super().__init__(parent)
        self._categorias = categorias or []
        # Definir columnas: (atributo, encabezado)
        self._colums = [
            ("id_categoria", "ID"),
            ("nombre", "Nombre"),
            ("descripcion", "Descripción")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._categorias)

    def columnCount(self, parent=QModelIndex()):
        return len(self._colums)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        categoria_obj = self._categorias[index.row()]
        attr, _header = self._colums[index.column()]

        # Obtener el valor del atributo
        valor = getattr(categoria_obj, attr, "")
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

    def setCategorias(self, categorias: list):
        """Actualizar la lista de categorias en el modelo"""
        self.beginResetModel()
        self._categorias = categorias
        self.endResetModel()

class CatWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self,empleado: Empleado):
        super().__init__()
        self.setupUi(self)
        self.categoriaController = CategoriaController()
        self.categoria = Categoria()
        self.categorias = None
        self.labelEmpleado.setText(f"Empleado: {empleado.nombre}")

        # Llenar el combo categorias
        self.comboCategorias.addItem("ID", "id_categoria")
        self.comboCategorias.addItem("Nombre", "nombre")
        self.comboCategorias.addItem("Descripcion", "descripcion")

        # Configurar el modelo para la tabla
        self._table_model = CategoriaTableModel()
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
            self.txtDescripcion.toPlainText().strip()
        ]:
            return
        categoria = Categoria(
            nombre=self.lineNombre.text().strip(),
            descripcion=self.txtDescripcion.toPlainText().strip()
        )
        mensaje = self.categoriaController.addCategoria(categoria)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()

    def handleEditarBtn(self):
        if self.categoria.id_categoria is None:
            return
        categoriaModificado = Categoria(
            id_categoria=self.categoria.id_categoria,
            nombre=self.lineNombre.text().strip(),
            descripcion=self.txtDescripcion.toPlainText().strip()
        )
        mensaje = self.categoriaController.updateCategoria(categoriaModificado)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()

    def handleBorrarBtn(self):
        if self.categoria.id_categoria is None:
            return
        self.categoriaController.deleteCategoria(self.categoria.id_categoria)
        self.labelInformacion.setText("Categoria Eliminado Exitosamente")
        self.limpiarCampos()
        self.mostrarTabla()

    def handleBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            self.categorias = self.categoriaController.buscar(columna, aBuscar)
        except Exception:
            self.categorias = None
        self.lineDato.clear()
        self.mostrarTabla()

    def mostrarTabla(self):
        """Cargar y mostrar las categorias en la tabla"""
        try:
            categorias = self.categorias or self.categoriaController.categorias()
            self._table_model.setCategorias(categorias)
            self.categorias = None
        except Exception as e:
            print(f"Error al cargar categorias: {e}")

    def handleDobleClic(self, index: QModelIndex):
        datos = []
        datos.extend(
            self._table_model.index(index.row(), nColumna, index).data()
            for nColumna in range(self._table_model.columnCount())
        )
        self.categoria = Categoria(
            id_categoria=datos[0],
            nombre=datos[1],
            descripcion=datos[2]
        )
        self.lineNombre.setText(self.categoria.nombre)
        self.txtDescripcion.setText(self.categoria.descripcion)

    def limpiarCampos(self):
        self.lineNombre.clear()
        self.txtDescripcion.clear()
        self.categoria = Categoria()

