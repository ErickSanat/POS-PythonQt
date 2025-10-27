from ..model import Promocion
from ..dao import PromocionDAO

class PromocionController:
    def __init__(self):
        self.promocionDAO = PromocionDAO()

    def promociones(self) -> list[Promocion]:
        return self.promocionDAO.promociones()

    def promocion(self, id_promocion: int) -> Promocion:
        return self.promocionDAO.promocion(id_promocion)

    def addPromocion(self, promocion: Promocion):
        if not self.promocionDAO.promocionExistente(promocion):
            self.promocionDAO.addPromocion(promocion)
            return "Añadido exitosamente"
        else:
            return "La receta ya existe"

    def updatePromocion(self, promocion: Promocion):
        self.promocionDAO.updatePromocion(promocion)

    def deletePromocion(self, id_promocion: int):
        self.promocionDAO.deletePromocion(id_promocion)

    def buscar(self, columna: str, aBuscar: str) -> list[Promocion]:
        try:
            return self.promocionDAO.buscarPromociones(columna, aBuscar)
        except Exception as e:
            raise e

    def porNombre(self, nombre: str) -> Promocion:
        return self.promocionDAO.porNombre(nombre)