from ..model import DetalleVenta, Venta, Producto
from ..dao import DetalleVentaDAO

class DetalleVentaController:
    def __init__(self):
        self.detalleVentaDAO = DetalleVentaDAO()
    
    def detalleVentas(self) -> list[DetalleVenta]:
        try:
            return self.detalleVentaDAO.detalleVentas()
        except Exception as e:
            raise e
    
    def detalleVenta(self, id_detalleVenta) -> DetalleVenta:
        try:
            return self.detalleVentaDAO.detalleVenta(id_detalleVenta)
        except Exception as e:
            raise e
    
    def addDetalleVenta(self, detalleVenta: DetalleVenta):
        self.detalleVentaDAO.addDetalleVenta(detalleVenta)
    
    def updateDetalleVenta(self, detalleVenta: DetalleVenta):
        self.detalleVentaDAO.updateDetalleVenta(detalleVenta)
    
    def deleteDetalleVenta(self, id_detalleVenta: int):
        self.detalleVentaDAO.deleteDetalleVenta(id_detalleVenta)

    def buscar(self, columna: str, aBuscar: str) -> list[DetalleVenta]:
        try:
            return self.detalleVentaDAO.buscarDetalleVentas(columna, aBuscar)
        except Exception as e:
            raise e
        
    def buscarPorVenta(self, venta: Venta) -> DetalleVenta:
        try:
            return self.detalleVentaDAO.buscarPorVenta(venta)
        except Exception as e:
            raise e