from .venta import Venta
from .tipoPago import TipoPago

class Pago:
    def __init__(
        self,
        id_pago: int=None,
        venta: Venta=None,
        tipo_pago: TipoPago=None,
        monto: float=None
    ):
        self.id_pago = id_pago
        self.venta = venta
        self.tipo_pago = tipo_pago
        self.monto = monto
    
    def __repr__(self):
        return f"""
    id_pago: {self.id_pago}
    venta: [{self.venta}]
    tipo_pago: [{self.tipo_pago}]
    monto: {self.monto}
"""