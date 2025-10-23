from ..model import Empleado, Usuario
from ..dao import EmpleadoDAO

class EmpleadoController:
    def __init__(self):
        self.empleadoDAO = EmpleadoDAO()
    
    def empleados(self) -> list[Empleado]:
        try:
            return self.empleadoDAO.empleados()
        except Exception as e:
            raise e
    
    def empleado(self, id_empleado) -> Empleado:
        try:
            return self.empleadoDAO.empleado(id_empleado)
        except Exception as e:
            raise e
    
    def addEmpleado(self, empleado: Empleado):
        self.empleadoDAO.addEmpleado(empleado)
    
    def updateEmpleado(self, empleado: Empleado):
        self.empleadoDAO.updateEmpleado(empleado)
    
    def deleteEmpleado(self, id_empleado: int):
        self.empleadoDAO.deleteEmpleado(id_empleado)

    def buscar(self, columna: str, aBuscar: str) -> list[Empleado]:
        try:
            return self.empleadoDAO.buscarEmpleados(columna, aBuscar)
        except Exception as e:
            raise e
        
    def buscarPorUsuario(self, usuario: Usuario) -> Empleado:
        try:
            return self.empleadoDAO.buscarPorUsuario(usuario)
        except Exception as e:
            raise e