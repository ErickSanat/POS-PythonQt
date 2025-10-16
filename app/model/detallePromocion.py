from .promocion import Promocion
from .producto import Producto
class DetallePromocion:
    def __init__(
        self,
        id_detalle_promocion: int=None,
        promocion: Promocion=None,
        producto: Producto=None
    ):
        self.id_detalle_promocion = id_detalle_promocion
        self.promocion = promocion
        self.producto = producto
    
    def __repr__(self):
        from json import dumps, loads
        return dumps(
            {
                "id_detalle_promocion": self.id_detalle_promocion,
                "promocion": loads(repr(self.promocion)),
                "producto": loads(repr(self.producto))
            }, indent=4
        )