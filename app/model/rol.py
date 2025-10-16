class Rol:
    def __init__(
        self,
        id_rol: int=None,
        nombre: str=None
    ):
        self.id_rol = id_rol
        self.nombre = nombre
        
    def __repr__(self):
        from json import dumps
        return dumps(
            {
                "id_rol": self.id_rol,
                "nombre": self.nombre
            }, indent=4
        )