from .categoria import Categoria
class Producto:
    def __init__(
        self,
        id_producto: int=None,
        nombre: str=None,
        descripcion: str=None,
        precio: float=None,
        stock: int=None,
        categoria: Categoria=None
    ):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
    
    def __repr__(self):
        from json import dumps, loads
        return dumps(
            {
                "id_producto": self.id_producto,
                "nombre": self.nombre,
                "descripcion": self.descripcion,
                "precio": float(self.precio),
                "stock": self.stock,
                "categoria": loads(repr(self.categoria))
            }, indent=4
        )
