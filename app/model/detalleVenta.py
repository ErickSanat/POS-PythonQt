from .venta import Venta
from .producto import Producto

class DetalleVenta:
    def __init__(
        self,
        id_detalle: int=None,
        venta: Venta=None,
        producto: Producto=None,
        cantidad: int=None,
        subtotal: float=None,
    ):
        self.id_detalle = id_detalle
        self.venta = venta
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = subtotal
    
    def __repr__(self):
        return f"""
    id_detalle: {self.id_detalle}
    venta: [{self.venta}]
    producto: [{self.producto}]
    cantidad: {self.cantidad}
    subtotal: {self.subtotal}
"""