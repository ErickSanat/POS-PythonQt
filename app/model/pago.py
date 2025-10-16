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
        from json import dumps, loads
        return dumps(
            {
                "id_pago": self.id_pago,
                "venta": loads(repr(self.venta)),
                "tipo_pago": loads(repr(self.tipo_pago)),
                "monto": float(self.monto)
            }, indent=4
        )