from .usuario import Usuario
from .cliente import Cliente
from datetime import datetime
class Venta:
    def __init__(
        self,
        id_venta: int=None,
        fecha: datetime=None,
        usuario: Usuario=None,
        cliente: Cliente=None,
        total: float=None,
    ):
        self.id_venta  = id_venta 
        self.fecha = fecha
        self.usuario  = usuario 
        self.cliente = cliente
        self.total = total
    
    def __repr__(self):
        return f"""
    id_venta: {self.id_venta}
    fecha: {self.fecha}
    usuario: [{self.usuario}]
    cliente: [{self.cliente}]
    total: {self.total}
"""
