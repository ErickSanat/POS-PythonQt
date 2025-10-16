from ..model import Empleado
from ..dao import EmpleadoDAO

class EmpleadoController:
    def __init__(self):
        self.empleadoDAO = EmpleadoDAO()
    
    def empleados(self) -> list[Empleado]:
        try:
            return self.empleadoDAO.empleados()
        except Exception as e:
            return e
    
    def empleado(self, id_empleado) -> Empleado:
        try:
            return self.empleadoDAO.empleado(id_empleado)
        except Exception as e:
            return e
    
    def addEmpleado(self, empleado: Empleado):
        self.empleadoDAO.addEmpleado(empleado)
    
    def updateEmpleado(self, empleado: Empleado):
        self.empleadoDAO.updateEmpleado(empleado)
    
    def deleteEmpleado(self, id_empleado: int):
        self.empleadoDAO.deleteEmpleado(id_empleado)