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
    def setProducto(self, producto: Producto):
        self.productoDAO.setProducto(producto)
