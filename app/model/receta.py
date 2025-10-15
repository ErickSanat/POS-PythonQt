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
        return f"""
    id: {self.id_receta}
    producto: [{self.producto}]
    descripcion: {self.descripcion}
    instrucciones: {self.instrucciones}
"""