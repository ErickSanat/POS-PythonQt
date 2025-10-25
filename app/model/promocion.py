class Promocion:
    def __init__(
        self,
        # checar si se puede meter enum
        id_promocion: int=None,
        nombre: str=None,
        porcentaje: int=None,
        descripcion: str=None
    ):
        self.id_promocion = id_promocion
        self.nombre = nombre
        self.porcentaje = porcentaje
        self.descripcion = descripcion
    
    def __repr__(self):
        from json import dumps
        return dumps(
            {
                "id_promocion": self.id_promocion,
                "nombre": self.nombre,
                "porcentaje": self.porcentaje,
                "descripcion": self.descripcion
            }, indent=4
        )