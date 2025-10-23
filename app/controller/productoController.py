from ..model import Producto
from ..dao import ProductoDAO

class ProductoController:
    def __init__(self):
        self.productoDAO = ProductoDAO()
    
    def productos(self) -> list[Producto]:
        try:
            return self.productoDAO.productos()
        except Exception as e:
            return e
    
    def producto(self, id_producto:int) -> Producto:
        try:
            return self.productoDAO.producto(id_producto)
        except Exception as e:
            return e
    def addProducto(self, producto: Producto) -> str:
        if not self.productoDAO.productoExistente(producto):
            self.productoDAO.addProducto(producto)
            return "Añadido exitosamente"
        else:
            return "El producto ya existe"
    
    def updateProducto(self, producto: Producto):
        self.productoDAO.updateProducto(producto)
    
    def deleteProducto(self, id_producto: int):
        self.productoDAO.deleteProducto(id_producto)

    def buscar(self, columna: str, aBuscar: str) -> list[Producto]:
        try:
            return self.productoDAO.buscarProductos(columna, aBuscar)
        except Exception as e:
            raise e