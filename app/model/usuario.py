from rol import Rol
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
    
