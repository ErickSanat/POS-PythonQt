from ..model import Proveedor
from ..dao import ProveedorDAO

class ProveedorController:
    def __init__(self):
        self.proveedorDAO = ProveedorDAO()

    def proveedores(self) -> list[Proveedor]:
        try:
            return self.proveedorDAO.proveedores()
        except Exception as e:
            raise e

    def proveedor(self, id_proveedor: int) -> Proveedor:
        try:
            return self.proveedorDAO.proveedor(id_proveedor)
        except Exception as e:
            raise e

    def addProveedor(self, proveedor: Proveedor):
        self.proveedorDAO.addProveedor(proveedor)

    def updateProveedor(self, proveedor: Proveedor):
        self.proveedorDAO.updateProveedor(proveedor)

    def deleteProveedor(self, id_proveedor: int):
        self.proveedorDAO.deleteProveedor(id_proveedor)

    def buscar(self, columna: str, aBuscar: str) -> list[Proveedor]:
        try:
            return self.proveedorDAO.buscarProveedores(columna, aBuscar)
        except Exception as e:
            raise e