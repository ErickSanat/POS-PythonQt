from .usuario import Usuario

class Empleado:
    def __init__(
        self,
        id_empleado: int=None,
        nombre: str=None,
        direccion: str=None,
        telefono: int=None,
        usuario: Usuario=None
    ):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.usuario = usuario
    
    def __repr__(self):
        from json import dumps, loads
        return dumps(
            {
                "id_empleado": self.id_empleado,
                "nombre": self.nombre,
                "direccion": self.direccion,
                "telefono": self.telefono,
                "usuario": loads(repr(self.usuario))
            }, indent=4
        )