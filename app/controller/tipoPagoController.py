from ..dao import TipoPagoDAO
from ..model import TipoPago

class TipoPagoController:
    def __init__(self):
        self.tipoPagoDAO = TipoPagoDAO()
    
    def tiposPago(self) -> list[TipoPago]:
        return self.tipoPagoDAO.tiposPago()
    
    def tipoPago(self, id_tipoPago: int) -> TipoPago:
        return self.tipoPagoDAO.tipoPago(id_tipoPago)
