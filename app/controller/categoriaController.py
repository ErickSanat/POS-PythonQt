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

    def addCategoria(self, categoria: Categoria):
        self.rolDAO.addCategoria(categoria)

    def updateCategoria(self, categoria: Categoria):
        self.rolDAO.updateCategoria(categoria)

    def deleteCategoria(self, id_categoria: int):
        self.rolDAO.deleteCategoria(id_categoria)

    def buscar(self, columna: str, aBuscar: str) -> list[Categoria]:
        try:
            return self.rolDAO.buscarCategorias(columna, aBuscar)
        except Exception as e:
            raise e