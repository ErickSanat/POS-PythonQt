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
        return f"""
    id: {self.id_producto}
    nombre: {self.nombre}
    descripcion: {self.descripcion}
    precio: {self.precio}
    stock: {self.stock}
    categoria: [{self.categoria}]
"""
