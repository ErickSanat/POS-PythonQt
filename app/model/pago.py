from .tipoPago import TipoPago

class Pago:
    def __init__(
        self,
        id_pago: int=None,
        tipo_pago: TipoPago=None,
        cantidad: float=None
    ):
        self.id_pago = id_pago
        self.tipo_pago = tipo_pago
        self.cantidad = cantidad
    
    def __repr__(self):
        from json import dumps, loads
        return dumps(
            {
                "id_pago": self.id_pago,
                "tipo_pago": loads(repr(self.tipo_pago)),
                "cantidad": float(self.cantidad)
            }, indent=4
        )