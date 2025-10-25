import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.recetaView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado, Receta, Producto
from app.controller import RecetaController, ProductoController

class RecetaTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Receta en un QTableView"""
    def __init__(self, recetas: list = None, parent=None):
        super().__init__(parent)
        self._recetas = recetas or []
        # Definir columnas: (atributo, encabezado)
        self._columns = [
            ("id_receta", "ID"),
            ("producto", "Producto"),
            ("descripcion", "Descripcion"),
            ("instrucciones", "Instrucciones")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._recetas)

    def columnCount(self, parent=QModelIndex()):
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        receta_obj = self._recetas[index.row()]
        attr, _header = self._columns[index.column()]
        if attr == "producto":
            producto = getattr(receta_obj, "producto", None)
            return str(producto.nombre) if producto is not None else ""
        valor = getattr(receta_obj, attr, "")
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

    def setRecetas(self, recetas: list):
        self.beginResetModel()
        self._recetas = recetas or []
        self.endResetModel()

class RecWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)
        self.recetaController = RecetaController()
        self.productoController = ProductoController()
        self.producto = Producto()
        self.receta = Receta()
        self.recetas = None
        for producto in self.productoController.productos():
            self.comboProductos.addItem(producto.nombre, producto.id_producto)

        self.comboCategorias.addItem("ID", "id_receta")
        self.comboCategorias.addItem("Producto", "nombre")
        self.comboCategorias.addItem("Descripcion", "descripcion")
        self.comboCategorias.addItem("Instrucciones", "instrucciones")

        # Configurar el modelo para la tabla
        self._table_model = RecetaTableModel()
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
        if self.descripcion.toPlainText().strip() == "" or self.instrucciones.toPlainText().strip() == "":
            return
        receta = Receta(
            None,
            Producto(self.comboProductos.currentData()),
            self.descripcion.toPlainText().strip(),
            self.instrucciones.toPlainText().strip()
        )
        mensaje = self.recetaController.addReceta(receta)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()

    def handleEditarBtn(self):
        if self.receta.id_receta is None:
            return
        recetaModificada = Receta(
            self.receta.id_receta,
            Producto(self.comboProductos.currentData()),
            self.descripcion.toPlainText().strip(),
            self.instrucciones.toPlainText().strip()
        )
        mensaje = self.recetaController.updateReceta(recetaModificada)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()

    def handleBorrarBtn(self):
        if self.receta.id_receta is None:
            return
        self.recetaController.deleteReceta(self.receta.id_receta)
        self.labelInformacion.setText("Receta Eliminado Exitosamente")
        self.limpiarCampos()
        self.mostrarTabla()

    def handelBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            self.recetas = self.recetaController.buscar(columna, aBuscar)
        except Exception:
            self.labelInformacion.setText("No se encontraron resultados")
        self.lineDato.clear()
        self.mostrarTabla()

    def handleDobleClic(self, index: QModelIndex):
        datos = []
        datos.extend(
            self._table_model.index(index.row(), nColumna, index).data()
            for nColumna in range(self._table_model.columnCount())
        )
        self.receta = Receta(
            datos[0],
            self.productoController.porNombre(datos[1]),
            datos[2],
            datos[3]
        )
        self.comboProductos.setCurrentText(self.receta.producto.nombre)
        self.descripcion.setText(self.receta.descripcion)
        self.instrucciones.setText(self.receta.instrucciones)

    def limpiarCampos(self):
        self.comboProductos.setCurrentIndex(0)
        self.descripcion.clear()
        self.instrucciones.clear()
        self.receta = Receta()

    def mostrarTabla(self):
        try:
            recetas = self.recetas or self.recetaController.recetas()
            self._table_model.setRecetas(recetas)
            self.recetas = None
        except Exception as e:
            print(f"Error al cargar recetas: {e}")