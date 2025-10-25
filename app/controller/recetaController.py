from ..model import Receta
from ..dao import  RecetaDAO

class RecetaController:
    def __init__(self):
        self.recetaDAO = RecetaDAO()

    def recetas(self) -> list[Receta]:
        return self.recetaDAO.recetas()

    def receta(self, id_receta: int) -> Receta:
        return self.recetaDAO.receta(id_receta)

    def addReceta(self, receta: Receta):
        if not self.recetaDAO.recetaExistente(receta):
            self.recetaDAO.addReceta(receta)
            return "Añadido exitosamente"
        else:
            return "La receta ya existe"

    def updateReceta(self, receta: Receta):
        self.recetaDAO.updateReceta(receta)

    def deleteReceta(self, id_receta: int):
        self.recetaDAO.deleteReceta(id_receta)

    def buscar(self, columna: str, aBuscar: str) -> list[Receta]:
        try:
            return self.recetaDAO.buscarRecetas(columna, aBuscar)
        except Exception as e:
            raise e

    def buscarPorProducto(self, producto: int) -> list[Receta]:
        try:
            return self.recetaDAO.buscarPorProducto(producto)
        except Exception as e:
            raise e
