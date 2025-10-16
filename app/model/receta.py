from .producto import Producto

class Receta:
    def __init__(
        self,
        id_receta: int=None,
        producto: Producto=None,
        descripcion: str=None,
        instrucciones: str=None
    ):
        self.id_receta = id_receta
        self.producto = producto
        self.descripcion = descripcion
        self.instrucciones = instrucciones
        
    def __repr__(self):
        from json import dumps, loads
        return dumps(
            {
                "id_receta": self.id_receta,
                "producto": loads(repr(self.producto)),
                "descripcion": self.descripcion,
                "instrucciones": self.instrucciones
            }, indent=4
        )