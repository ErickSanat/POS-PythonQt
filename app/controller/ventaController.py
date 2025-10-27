from ..model import Venta, Empleado, Cliente, Promocion, Pago
from ..dao import VentaDAO

class VentaController:
    def __init__(self):
        self.ventaDAO = VentaDAO()

    def ventas(self) -> list[Venta]:
        try:
            return self.ventaDAO.ventas()
        except Exception as e:
            raise e

    def venta(self, id_venta: int) -> Venta:
        try:
            return self.ventaDAO.venta(id_venta)
        except Exception as e:
            raise e

    def addVenta(self, venta: Venta):
        self.ventaDAO.addVenta(venta)

    def ultimoVenta(self) -> Venta:
        return self.ventaDAO.ultimaVenta()

    def buscar(self, columna: str, aBuscar: str) -> list[Venta]:
        try:
            return self.ventaDAO.buscarVentas(columna, aBuscar)
        except Exception as e:
            raise e

    def buscarPorEmpleado(self, empleado: Empleado) -> list[Venta]:
        try:
            return self.ventaDAO.buscarPorEmpleado(empleado)
        except Exception as e:
            raise e

    def buscarPorCliente(self, cliente: Cliente) -> list[Venta]:
        try:
            return self.ventaDAO.buscarPorCliente(cliente)
        except Exception as e:
            raise e

    def buscarPorPromocion(self, promocion: Promocion) -> list[Venta]:
        try:
            return self.ventaDAO.buscarPorPromocion(promocion)
        except Exception as e:
            raise e

    def buscarPorPago(self, pago: Pago) -> list[Venta]:
        try:
            return self.ventaDAO.buscarPorPago(pago)
        except Exception as e:
            raise e