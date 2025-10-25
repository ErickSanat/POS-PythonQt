from .empleado import Empleado
from .cliente import Cliente
from .pago import Pago
from .promocion import Promocion
from datetime import datetime
class Venta:
    def __init__(
        self,
        id_venta: int=None,
        fecha: datetime=None,
        empleado: Empleado=None,
        cliente: Cliente=None,
        promocion: Promocion=None,
        pago: Pago=None,
        total: float=None,
    ):
        self.id_venta  = id_venta 
        self.fecha = fecha
        self.empleado  = empleado 
        self.cliente = cliente
        self.promocion = promocion
        self.pago = pago
        self.total = total
    
    def __repr__(self):
        from json import dumps, loads
        return dumps(
            {
                "id_venta": self.id_venta,
                "fecha": self.fecha,
                "empleado": loads(repr(self.empleado)),
                "cliente": loads(repr(self.cliente)),
                "promocion": loads(repr(self.promocion)),
                "pago": loads(repr(self.pago)),
                "total": float(self.total),
            }, indent=4
        )