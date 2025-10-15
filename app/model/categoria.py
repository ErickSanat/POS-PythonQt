class Categoria:
    def __init__(
        self,
        id_categoria: int=None,
        nombre: str=None,
        descripcion: str=None
    ):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion
    
    def __repr__(self):
        return f"""
    id: {self.id_categoria}
    nombre: {self.nombre}
    descripcion: {self.descripcion}
"""