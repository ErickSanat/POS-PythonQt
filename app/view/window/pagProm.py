import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from ..generated.promocionView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado, Promocion
from app.controller import PromocionController

class PromocionTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Promocion en un QTableView"""
    def __init__(self, promociones: list = None, parent=None):
        super().__init__(parent)
        self._promociones = promociones or []
        # Definir columnas: (atributo, encabezado)
        self._colums = [
            ("id_promocion", "ID"),
            ("nombre", "Nombre"),
            ("porcentaje", "Porcentaje"),
            ("descripcion", "Descripción")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._promociones)

    def columnCount(self, parent=QModelIndex()):
        return len(self._colums)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        promocion = self._promociones[index.row()]
        attr, _header = self._colums[index.column()]
        valor = getattr(promocion, attr, "")
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

    def setPromociones(self, promociones: list):
        """Actualizar la lista de promociones en el modelo"""
        self.beginResetModel()
        self._promociones = promociones or []
        self.endResetModel()

class PromWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)
        self.promocionController = PromocionController()
        self.promocion = Promocion()
        self.promociones = None

        self.comboCategorias.addItem("ID", "id_promocion")
        self.comboCategorias.addItem("Nombre", "nombre")
        self.comboCategorias.addItem("Porcentaje", "porcentaje")
        self.comboCategorias.addItem("Descripcion", "descripcion")

        # Configurar el modelo para la tabla
        self._table_model = PromocionTableModel()
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

        #Configurar el menú flotante
        self.setupFloatingMenu(empleado)
        self.mostrarTabla()

    def handleAgregarBtn(self):
        if "" in [
            self.lineNombre.text().strip(),
            self.linePorcentaje.text().strip(),
            self.lineDescripcion.text().strip()
        ]:
            return
        promocion = Promocion(
            None,
            self.lineNombre.text().strip(),
            self.linePorcentaje.text().strip(),
            self.lineDescripcion.text().strip()
        )
        mensaje = self.promocionController.addPromocion(promocion)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()

    def handleEditarBtn(self):
        if self.promocion.id_promocion is None:
            return
        promocionModificada = Promocion(
            self.promocion.id_promocion,
            self.lineNombre.text().strip(),
            self.linePorcentaje.text().strip(),
            self.lineDescripcion.text().strip()
        )
        mensaje = self.promocionController.updatePromocion(promocionModificada)
        self.labelInformacion.setText(mensaje)
        self.limpiarCampos()
        self.mostrarTabla()

    def handleBorrarBtn(self):
        if self.promocion.id_promocion is None:
            return
        self.promocionController.deletePromocion(self.promocion.id_promocion)
        self.labelInformacion.setText("Promocion Eliminado Exitosamente")
        self.limpiarCampos()
        self.mostrarTabla()

    def handelBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            self.promociones = self.promocionController.buscar(columna, aBuscar)
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
        self.promocion = Promocion(
            datos[0],
            datos[1],
            datos[2],
            datos[3]
        )
        self.lineNombre.setText(self.promocion.nombre)
        self.linePorcentaje.setText(self.promocion.porcentaje)
        self.lineDescripcion.setText(self.promocion.descripcion)

    def limpiarCampos(self):
        self.lineNombre.clear()
        self.linePorcentaje.clear()
        self.lineDescripcion.clear()
        self.promocion = Promocion()

    def mostrarTabla(self):
        try:
            promociones = self.promociones or self.promocionController.promociones()
            self._table_model.setPromociones(promociones)
            self.promociones = None
        except Exception as e:
            print(f"Error al cargar promociones: {e}")
