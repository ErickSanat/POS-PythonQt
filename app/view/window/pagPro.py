import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QSize
from ..generated.productoView_ui import Ui_Form
from app.utils import MenuFlotante
from app.model import Empleado, Producto, Categoria
from app.controller import ProductoController, CategoriaController
import os, shutil

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
        if not index.isValid():
            return QVariant()

        producto = self._productos[index.row()]
        attr, _header = self._columns[index.column()]

        # Manejo especial para la columna "categoria"
        if attr == "categoria":
            if role == Qt.DisplayRole:
                categoria = getattr(producto, "categoria", None)
                return categoria.nombre if categoria else ""
            return QVariant()

        # Manejo especial para la columna "imagen"
        if attr == "imagen":
            img_val = getattr(producto, "imagen", None)

            # DecorationRole: mostrar el icono/imagen
            if role == Qt.DecorationRole:
                if not img_val:
                    return QVariant()

                pix = QPixmap()
                try:
                    pix.load(img_val)
                except Exception as e:
                    print(f"Error cargando imagen: {e}")
                    return QVariant()

                if pix.isNull():
                    return QVariant()

                # Escalar y devolver como icono
                return QIcon(pix.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
            return QVariant()

        # Para el resto de columnas normales
        if role == Qt.DisplayRole:
            valor = getattr(producto, attr, "")
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
        self.archivo = None
        
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
        
        # ToDo: meter esto a un for para ahorrar espacio
        self.comboCategorias.addItem("ID", "id_producto")
        self.comboCategorias.addItem("Nombre", "nombre")
        self.comboCategorias.addItem("Descripcion", "descripcion")
        self.comboCategorias.addItem("Precio", "precio")
        self.comboCategorias.addItem("Stock", "stock")
        # ToDo: agregar filtro de imagen
        # self.comboCategorias.addItem("Imagen", "imagen")
        self.comboCategorias.addItem("Categoria", "nombre")
        
        self.setupFloatingMenu(empleado)
        self.mostrarTabla()
        
        # Configurar apariencia de la tabla
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        self.tableView.doubleClicked.connect(self.handleDobleClic)
        
        self.btnAgregar.clicked.connect(self.handleAgregarBtn)
        self.btnEditar.clicked.connect(self.handleEditarBtn)
        self.btnEliminar.clicked.connect(self.handleBorrarBtn)
        self.btnBuscar.clicked.connect(self.handelBuscarBtn)
        self.btnImagen.clicked.connect(self.handleImagenBtn)
    
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
        # Copiar imagen
        shutil.copy(self.archivo, producto.imagen)
        mensaje = self.productoController.addProducto(producto)
        
        self.labelInformacion.setText(mensaje)
        self.lineNombre.clear()
        self.descripcion.clear()
        self.linePrecio.clear()
        self.lineStock.clear()
        self.rutaImagen.clear()
        self.archivo = None
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
        # Cambiar imagen
        if self.producto.imagen != productoModificado.imagen:
            os.remove(self.producto.imagen)
            shutil.copy(self.archivo, productoModificado.imagen)
        
        self.productoController.updateProducto(productoModificado)
        self.labelInformacion.setText("Producto Actualizado Exitosamente")
        self.lineNombre.clear()
        self.descripcion.clear()
        self.linePrecio.clear()
        self.lineStock.clear()
        self.rutaImagen.clear()
        self.archivo = None
        self.mostrarTabla()
    
    def handleBorrarBtn(self):
        if self.producto.id_producto is None:
            return
        self.productoController.deleteProducto(self.producto.id_producto)
        os.remove(self.producto.imagen)
        
        self.labelInformacion.setText("Producto Eliminado Exitosamente")
        self.lineNombre.clear()
        self.descripcion.clear()
        self.linePrecio.clear()
        self.lineStock.clear()
        self.rutaImagen.clear()
        self.archivo = None
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
            self.productoController.producto(datos[0]).imagen,
            self.categoriaController.porNombre(datos[6])
        )
        self.lineNombre.setText(self.producto.nombre)
        self.descripcion.setText(self.producto.descripcion)
        self.linePrecio.setText(self.producto.precio)
        self.lineStock.setText(self.producto.stock)
        self.rutaImagen.setText(self.producto.imagen)
        self.comboCategoria.setCurrentText(self.producto.categoria.nombre)

    def handleImagenBtn(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if archivo:

            carpeta_destino = "app/assets/productos"
            os.makedirs(carpeta_destino, exist_ok=True)
            nombre_archivo = os.path.basename(archivo)
            ruta_destino = os.path.join(carpeta_destino, f"{self.lineNombre.text().strip().replace(" ", "_")}_{nombre_archivo}")
            
            self.archivo = archivo
            self.rutaImagen.setText(ruta_destino)