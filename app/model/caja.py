from usuario import Usuario
from datetime import datetime

class Caja:
    def __init__(
        self,
        id_caja: int=None,
        fecha_apertura: datetime=None,
        fecha_cierre: datetime=None,
        monto_inicial: float=None,
        monto_final: float=None,
        estado: str="abierta",
        usuario: Usuario=None
    ):
        self.id_caja = id_caja
        self.fecha_apertura = fecha_apertura
        self.fecha_cierre = fecha_cierre
        self.monto_inicial = monto_inicial
        self.monto_final = monto_final
        self.estado = estado
        self.usuario = usuario