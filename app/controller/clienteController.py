from ..model import Cliente
from .. dao import ClienteDAO

class ClienteController:
    def __init__(self):
        self.clienteDAO = ClienteDAO()

    def clientes(self) -> list[Cliente]:
        try:
            return self.clienteDAO.clientes()
        except Exception:
            return []

    def cliente(self, id_cliente: int) -> Cliente|None:
        try:
            return self.clienteDAO.cliente(id_cliente)
        except Exception:
            return None

    def addCliente(self, cliente: Cliente) -> str:
        if not self.clienteDAO.clienteExistente(cliente):
            self.clienteDAO.addCliente(cliente)
            return "Añadido exitosamente"
        else:
            return "El cliente ya existe"

    def updateCliente(self, cliente: Cliente):
        self.clienteDAO.updateCliente(cliente)

    def deleteCliente(self, id_cliente: int):
        self.clienteDAO.deleteCliente(id_cliente)

    def buscar(self, columna: str, aBuscar: str) -> list[Cliente]:
        try:
            return self.clienteDAO.buscarClientes(columna, aBuscar)
        except Exception as e:
            raise e

    def porNombre(self, nombre: str) -> Cliente:
        return self.clienteDAO.porNombre(nombre)