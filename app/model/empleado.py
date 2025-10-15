from usuario import Usuario

class Empelado:
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