class Rol:
    def __init__(
        self,
        id_rol: int=None,
        nombre: str=None
    ):
        self.id_rol = id_rol
        self.nombre = nombre
        
    def __repr__(self):
        return f"""
    id: {self.id_rol}
    nombre: {self.nombre}
"""
