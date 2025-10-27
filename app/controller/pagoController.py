from ..model import Pago
from ..dao import PagoDAO

class PagoController:
    def __init__(self):
        self.pagoDAO = PagoDAO()

    def pagos(self) -> list[Pago]:
        try:
            return self.pagoDAO.pagos()
        except Exception as e:
            raise e

    def pago(self, id_pago: int) -> Pago:
        try:
            return self.pagoDAO.pago(id_pago)
        except Exception as e:
            raise e