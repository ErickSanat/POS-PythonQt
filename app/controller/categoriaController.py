from ..model import Categoria
from ..dao import CategoriaDAO

class CategoriaController:
    def __init__(self):
        self.rolDAO = CategoriaDAO()
    
    def categorias(self) -> list[Categoria]:
        return self.rolDAO.categorias()
    
    def categoria(self, id_categoria: int) -> Categoria:
        return self.rolDAO.categoria(id_categoria)
    
    def porNombre(self, nombre: str) -> Categoria:
        return self.rolDAO.porNombre(nombre)