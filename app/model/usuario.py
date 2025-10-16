from .rol import Rol
class Usuario:
    def __init__(
        self, 
        id_usuario: int=None, 
        usuario: str=None, 
        contrasena: str=None, 
        rol: Rol=None
    ):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol
    
    def __repr__(self):
        from json import dumps, loads
        return dumps(
            {
                "id_usuario": self.id_usuario,
                "usuario": self.usuario,
                "contrasena": self.contrasena,
                "rol": loads(repr(self.rol))
            }, indent=4
        )