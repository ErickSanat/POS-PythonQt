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
        from json import dumps
        return dumps(
            {
                "id_categoria": self.id_categoria,
                "nombre": self.nombre,
                "descripcion": self.descripcion
            }, indent=4
        )
