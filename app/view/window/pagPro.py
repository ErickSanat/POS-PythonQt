import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from ..generated.productoView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado, Producto, Categoria
from app.controller import ProductoController, CategoriaController

class ProductoTableModel(QAbstractTableModel):
    """Modelo para mostrar una lista de objetos Producto en un QTableView"""
    def __init__(self, productos: list[Producto] = None, parent=None):
        super().__init__(parent)
        self._productos = productos or []
        # Ajusta columnas según atributos reales de tu modelo Producto
        self._columns = [
            ("id_producto", "ID"),
            ("nombre", "Nombre"),
            ("descripcion", "Descripcion"),
            ("precio", "Precio"),
            ("stock", "Stock"),
            ("imagen", "Imagen"),
            ("categoria", "Categoria")
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self._productos)

    def columnCount(self, parent=QModelIndex()):
        return len(self._columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        producto = self._productos[index.row()]
        attr, _header = self._columns[index.column()]
        
        if attr == "categoria":
            categoria = getattr(producto, "categoria", None)
            return categoria.nombre if categoria else ""
        # Columna imagen: devolver icono en DecorationRole, texto en DisplayRole
        if attr == "imagen":
            img_val = getattr(producto, "imagen", None)
            if role == Qt.DecorationRole:
                if img_val is None or img_val == "":
                    return QVariant()
                pix = QPixmap(img_val)
                if pix.isNull():
                    return QVariant()
                # escalar y devolver icono
                return QIcon(pix.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            return QVariant()

        # Obtener valor del atributo
        valor = getattr(producto, attr, "")
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

    def setProductos(self, productos: list):
        self.beginResetModel()
        self._productos = productos or []
        self.endResetModel()

class ProWindow(QMainWindow, Ui_Form, MenuFlotante):
    def __init__(self, empleado: Empleado):
        super().__init__()
        self.setupUi(self)

        self.productoController = ProductoController()
        self.categoriaController = CategoriaController()
        
        self.producto = Producto()
        self.productos = None
        
        self._table_model = ProductoTableModel([])
        # Asegúrate que en tu UI el widget se llame 'tableView'; si no, cambia el nombre
        try:
            self.tableView.setModel(self._table_model)
            # tamaño del icono que se mostrará en la celda imagen
            self.tableView.setIconSize(QSize(64, 64))
            # ajustar alto de fila para que quepa la imagen
            self.tableView.verticalHeader().setDefaultSectionSize(72)
            self.tableView.horizontalHeader().setStretchLastSection(True)
            self.tableView.setAlternatingRowColors(True)
            self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        except Exception:
            # Si la UI no tiene tableView con ese nombre, evita crash y avisa por consola
            print("Aviso: tableView no encontrado en la UI. Ajusta el nombre del widget.")

        for categoria in self.categoriaController.categorias():
            self.comboCategoria.addItem(categoria.nombre, categoria.id_categoria)
        
        self.setupFloatingMenu(empleado)
        self.mostrarTabla()
        
        self.btnAgregar.clicked.connect(self.handleAgregarBtn)
        self.btnEditar.clicked.connect(self.handleEditarBtn)
        self.btnEliminar.clicked.connect(self.handleBorrarBtn)
    
    def handleAgregarBtn(self):
        if "" in [
            self.lineNombre.text().strip(),
            self.descripcion.toPlainText().strip(),
            self.linePrecio.text().strip(),
            self.lineStock.text().strip(),
            self.rutaImagen.text().strip(),
            ]:
            return
        producto = Producto(
            nombre=self.lineNombre.text().strip(),
            descripcion=self.descripcion.toPlainText().strip(),
            precio=self.linePrecio.text().strip(),
            stock=self.lineStock.text().strip(),
            imagen=self.rutaImagen.text().strip(),
            categoria=Categoria(self.comboCategoria.currentData(), self.comboCategoria.currentText())
        )
        mensaje = self.productoController.addProducto(producto)
        self.labelInformacion.setText(mensaje)
        self.lineNombre.clear()
        self.descripcion.clear()
        self.linePrecio.clear()
        self.lineStock.clear()
        self.rutaImagen.clear()
        self.mostrarTabla()

    def handleEditarBtn(self):
        if self.producto.id_producto is None:
            return
        productoModificado = Producto(
            self.producto.id_producto,
            self.lineNombre.text().strip(),
            self.descripcion.toPlainText().strip(),
            self.linePrecio.text().strip(),
            self.lineStock.text().strip(),
            self.rutaImagen.text().strip(),
            Categoria(self.comboCategoria.currentData(), self.comboCategoria.currentText())
        )
        self.productoController.updateProducto(productoModificado)
        self.labelInformacion.setText("Producto Actualizado Exitosamente")
        self.lineNombre.clear()
        self.descripcion.clear()
        self.linePrecio.clear()
        self.lineStock.clear()
        self.rutaImagen.clear()
        self.mostrarTabla()
    
    def handleBorrarBtn(self):
        if self.producto.id_producto is None:
            return
        self.productoController.deleteProducto(self.producto.id_producto)
        self.labelInformacion.setText("Producto Eliminado Exitosamente")
        self.lineNombre.clear()
        self.descripcion.clear()
        self.linePrecio.clear()
        self.lineStock.clear()
        self.rutaImagen.clear()
        self.mostrarTabla()
    
    def handelBuscarBtn(self):
        columna = self.comboCategorias.currentData()
        aBuscar = self.lineDato.text().strip()
        try:
            self.productos = self.productoController.buscar(columna, aBuscar)
        except Exception:
            self.productos = None
        self.lineDato.clear()
        self.mostrarTabla()

    def mostrarTabla(self):
        """Carga productos desde el controller y los muestra en el TableView"""
        try:
            productos = self.productos or self.productoController.productos()
            self._table_model.setProductos(productos)
            self.productos = None
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            
    
    def handleDobleClic(self, index: QModelIndex):
        datos = []
        datos.extend(
            self._table_model.index(index.row(), nColumna, index).data()
            for nColumna in range(self._table_model.columnCount())
        )
        self.producto = Producto(
            datos[0],
            datos[1],
            datos[2],
            datos[3],
            datos[4],
            datos[5],
            self.categoriaController.porNombre(datos[6])
        )
        self.lineNombre.setText(self.producto.nombre)
        self.descripcion.setText(self.producto.descripcion)
        self.linePrecio.setText(self.producto.precio)
        self.lineStock.setText(self.producto.stock)
        self.rutaImagen.setText(self.producto.imagen)
        self.comboCategoria.setCurrentText(self.producto.categoria.nombre)

