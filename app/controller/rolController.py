from ..model import Rol
from ..dao import RolDAO

class RolController:
    def __init__(self):
        self.rolDAO = RolDAO()
    
    def roles(self) -> list[Rol]:
        return self.rolDAO.roles()
    
    def rol(self, id_rol: int) -> Rol:
        return self.rolDAO.rol(id_rol)
    
    def porNombre(self, nombre: str) -> Rol:
        return self.rolDAO.porNombre(nombre)